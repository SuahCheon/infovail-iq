"""
filter_posts.py
---------------
naver_posts.db에 is_relevant 필터를 소급 적용한다.

동작:
  - posts 테이블에 `is_relevant` INTEGER 컬럼 추가 (없으면)
  - 전체 포스트에 필터 적용 후 0/1 기록
  - news 채널 포스트는 별도 테이블로 백업 후 삭제
  - 필터 탈락(is_relevant=0) 포스트는 삭제하지 않고 플래그만 기록
    -> 원본 보존, 분석 쿼리에서 WHERE is_relevant=1 조건 추가

Usage:
    python scripts/filter_posts.py
    python scripts/filter_posts.py --apply   # 실제 DB 수정 (기본: dry-run)
"""

import sqlite3
import argparse
from pathlib import Path
import sys

BASE_DIR = Path(r"C:\infovail-iq")
sys.path.insert(0, str(BASE_DIR))

from pipeline.config import DB_PATH

NAVER_DB = DB_PATH

from pipeline.ingestion.preprocessor import is_relevant


def run(db_path: Path, apply: bool) -> None:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # is_relevant 컬럼 추가 (없으면)
    cols = [r[1] for r in cur.execute("PRAGMA table_info(posts)").fetchall()]
    if "is_relevant" not in cols:
        if apply:
            cur.execute("ALTER TABLE posts ADD COLUMN is_relevant INTEGER DEFAULT NULL")
            print("컬럼 추가: is_relevant")
        else:
            print("[dry-run] ALTER TABLE posts ADD COLUMN is_relevant")

    # 전체 포스트 로드 (DB에 title 컬럼 없음 -> content만 사용)
    rows = cur.execute(
        "SELECT post_id, channel, content FROM posts"
    ).fetchall()
    print(f"총 포스트: {len(rows)}건")

    # 필터 적용
    results: dict[str, list] = {
        "pass": [], "channel": [], "boilerplate": [],
        "hard_exclude": [], "no_must_have": []
    }
    for row in rows:
        _, reason = is_relevant(
            row["channel"] or "",
            "",                    # title (DB에 없음)
            row["content"] or ""
        )
        results[reason].append(row["post_id"])

    # 집계 출력
    print(f"\n=== 필터 결과 ===")
    print(f"  통과 (is_relevant=1) : {len(results['pass']):>5}건")
    print(f"  채널 제외 (news)     : {len(results['channel']):>5}건")
    print(f"  boilerplate 스팸     : {len(results['boilerplate']):>5}건")
    print(f"  완전무관 제외        : {len(results['hard_exclude']):>5}건")
    print(f"  핵심어 미포함        : {len(results['no_must_have']):>5}건")
    total_out = sum(len(v) for k, v in results.items() if k != "pass")
    print(f"  탈락 소계            : {total_out:>5}건")
    print(f"  잔존 비율            : {len(results['pass'])/len(rows):.1%}")

    if not apply:
        print(f"\n[dry-run] 실제 적용하려면 --apply 플래그 추가")
        conn.close()
        return

    # is_relevant 플래그 업데이트
    cur.executemany(
        "UPDATE posts SET is_relevant=1 WHERE post_id=?",
        [(pid,) for pid in results["pass"]]
    )
    for reason, pids in results.items():
        if reason == "pass":
            continue
        cur.executemany(
            "UPDATE posts SET is_relevant=0 WHERE post_id=?",
            [(pid,) for pid in pids]
        )

    # news 채널 백업 테이블 생성 후 이동
    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts_news_backup AS
        SELECT * FROM posts WHERE 1=0
    """)
    cur.execute("""
        INSERT OR IGNORE INTO posts_news_backup
        SELECT * FROM posts WHERE channel = 'news'
    """)
    news_count = cur.execute(
        "SELECT COUNT(*) FROM posts WHERE channel='news'"
    ).fetchone()[0]
    cur.execute("DELETE FROM posts WHERE channel = 'news'")
    print(f"\nnews 채널 {news_count}건 -> posts_news_backup 이동 후 삭제")

    conn.commit()
    conn.close()

    print(f"\n완료: {db_path}")
    print(f"   분석 쿼리에 WHERE is_relevant=1 조건 추가 필요")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true",
                        help="실제 DB 수정 (없으면 dry-run)")
    args = parser.parse_args()
    run(NAVER_DB, apply=args.apply)


if __name__ == "__main__":
    main()
