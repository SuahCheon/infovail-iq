"""
remove_noise.py

목적: DB에서 "백신 오염" 키워드 게시물 삭제
      (백업 확인 후 DELETE 실행)
"""

import sqlite3
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DB_PATH     = Path("data/processed/naver_posts.db")
NOISE_KW    = "백신 오염"


def main():
    # 백업 확인
    backups = list(Path("data/processed").glob("*.backup_*.db"))
    if not backups:
        print("[ERROR] 백업 DB가 없습니다. 삭제를 중단합니다.")
        print("        merge_db.py를 먼저 실행해 백업을 만드세요.")
        return

    print(f"백업 확인: {[b.name for b in backups]}")

    conn = sqlite3.connect(DB_PATH)

    before = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    noise  = conn.execute(
        "SELECT COUNT(*) FROM posts WHERE keyword = ?", (NOISE_KW,)
    ).fetchone()[0]

    print(f"\nDB 전체: {before}건")
    print(f"삭제 대상 ('{NOISE_KW}'): {noise}건")

    if noise == 0:
        print("삭제 대상 없음. 종료.")
        conn.close()
        return

    confirm = input(f"\n'{NOISE_KW}' {noise}건을 삭제할까요? [y/N] ").strip().lower()
    if confirm != "y":
        print("취소.")
        conn.close()
        return

    conn.execute("DELETE FROM posts WHERE keyword = ?", (NOISE_KW,))
    conn.commit()

    after = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    print(f"\n삭제 완료: {before} -> {after}건 ({before - after}건 제거)")

    print("\n채널별 현황:")
    for ch, n in conn.execute(
        "SELECT channel, COUNT(*) FROM posts GROUP BY channel ORDER BY channel"
    ).fetchall():
        print(f"  {ch:<18} {n:>5}건")

    print("\n키워드별 현황:")
    for kw, n in conn.execute(
        "SELECT keyword, COUNT(*) FROM posts GROUP BY keyword ORDER BY COUNT(*) DESC"
    ).fetchall():
        print(f"  {kw:<26} {n:>5}건")

    conn.close()
    print("\n[OK] DB 노이즈 제거 완료.")


if __name__ == "__main__":
    main()
