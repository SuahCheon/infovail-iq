"""
merge_db.py

목적: 루트 naver_posts.db (기존 4,855건)를
      통합 DB에 병합.

실행: python scripts/merge_db.py
"""

import sqlite3
import shutil
from datetime import datetime
from pathlib import Path

SRC_DB  = Path(r"C:\infovail-iq\data\processed\naver_posts.db")
DST_DB  = Path(r"C:\infovail-iq\data\processed\naver_posts.db")
BACKUP  = DST_DB.with_suffix(f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")

def main():
    # -- 사전 확인 -------------------------------------------------
    if not SRC_DB.exists():
        print(f"[ERROR] 소스 DB 없음: {SRC_DB}")
        return
    if not DST_DB.exists():
        print(f"[ERROR] 대상 DB 없음: {DST_DB}")
        return

    src = sqlite3.connect(SRC_DB)
    dst = sqlite3.connect(DST_DB)

    src_count = src.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    dst_count = dst.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    print(f"통합 전 — 소스: {src_count}건 / 대상: {dst_count}건")

    # -- 대상 DB 백업 ----------------------------------------------
    shutil.copy2(DST_DB, BACKUP)
    print(f"백업 완료: {BACKUP.name}")

    # -- 소스 -> 대상으로 INSERT OR IGNORE -------------------------
    rows = src.execute("SELECT * FROM posts").fetchall()
    inserted = 0
    skipped  = 0

    for row in rows:
        try:
            dst.execute("""
                INSERT INTO posts
                    (post_id, channel, content, author_hash,
                     published_at, keyword, collected_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, row)
            inserted += 1
        except sqlite3.IntegrityError:
            skipped += 1

    dst.commit()
    src.close()

    final_count = dst.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    print(f"\n통합 결과")
    print(f"  신규 삽입: {inserted}건")
    print(f"  중복 스킵: {skipped}건")
    print(f"  최종 합계: {final_count}건")

    # -- 채널/날짜별 분포 ------------------------------------------
    print("\n채널별 합계:")
    for ch, n in dst.execute(
        "SELECT channel, COUNT(*) FROM posts GROUP BY channel ORDER BY channel"
    ).fetchall():
        print(f"  {ch:<18} {n:>5}건")

    print("\n날짜별 분포 (전체):")
    print(f"  {'날짜':<12} {'건수':>5}  이벤트")
    print(f"  {'-'*12} {'-'*5}  {'-'*20}")
    for d, n in dst.execute(
        "SELECT date(published_at), COUNT(*) FROM posts GROUP BY date(published_at) ORDER BY date(published_at)"
    ).fetchall():
        tag = ""
        if d and d == "2026-02-23": tag = "<-- 감사원 발표"
        if d and d == "2026-03-02": tag = "<-- SBS 보도"
        if d and d == "2026-03-04": tag = "<-- 코백회 기자회견"
        print(f"  {d:<12} {n:>5}  {tag}")

    dst.close()
    print("\n[OK] 통합 완료. data/processed/naver_posts.db 기준.")

if __name__ == "__main__":
    main()
