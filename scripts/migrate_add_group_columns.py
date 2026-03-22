"""
migrate_add_group_columns.py
-----------------------------
posts 테이블에 keyword_group, accountability_flag 컬럼 추가
- keyword_group: FM_Direct / Court / Chronic (keyword 기반 자동 매핑)
- accountability_flag: 1 = "정은경 백신" 키워드, 0 = 나머지
실행 전 백업을 먼저 수행합니다.
Usage:
    python migrate_add_group_columns.py
    python migrate_add_group_columns.py --db /path/to/naver_posts.db
    python migrate_add_group_columns.py --dry-run  # 실제 변경 없이 결과만 미리 확인
"""
import sqlite3
import argparse
import shutil
from datetime import datetime
from pathlib import Path

DEFAULT_DB = r"C:\infovail-iq\data\processed\naver_posts.db"

# 키워드 → 그룹 매핑 (단일 소스 오브 트루스)
KEYWORD_GROUP_MAP = {
    # FM_Direct
    "코로나 백신 이물질": "FM_Direct",
    "코로나 백신 곰팡이": "FM_Direct",
    "감사원 백신":        "FM_Direct",
    "정은경 백신":        "FM_Direct",   # accountability subtype
    # Court
    "코로나 백신 소송":       "Court",
    "백신 심근경색 판결":     "Court",
    "코로나 백신 항소":       "Court",
    "질병청 항소":            "Court",
    "코백회":                 "Court",
    "백신 피해 법원":         "Court",
    "코로나 백신 사망 판결":  "Court",
    # Chronic
    "코로나 백신 피해":         "Chronic",
    "백신 피해 보상":           "Chronic",
    "코로나 백신 부작용":       "Chronic",
    "백신 피해자 모임":         "Chronic",
    "코로나 백신 정부 책임":    "Chronic",
    "백신 피해자":              "Chronic",
}

ACCOUNTABILITY_KEYWORDS = {"정은경 백신"}


def backup_db(db_path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = db_path.parent / f"{db_path.stem}.backup_{ts}.db"
    shutil.copy2(db_path, backup_path)
    return backup_path


def main(db_path: str, dry_run: bool):
    path = Path(db_path)
    if not path.exists():
        print(f"[ERROR] DB 파일을 찾을 수 없음: {db_path}")
        return

    # ── 백업 ──────────────────────────────────────────────────────────────────
    if not dry_run:
        backup_path = backup_db(path)
        print(f"[백업] {backup_path}")
    else:
        print("[DRY-RUN] 백업 생략 (실제 변경 없음)")

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # ── 현재 컬럼 확인 ─────────────────────────────────────────────────────────
    cur.execute("PRAGMA table_info(posts)")
    existing_columns = {row[1] for row in cur.fetchall()}
    print(f"\n[현재 컬럼] {sorted(existing_columns)}")

    # ── 컬럼 추가 ─────────────────────────────────────────────────────────────
    columns_to_add = []
    if "keyword_group" not in existing_columns:
        columns_to_add.append(("keyword_group", "TEXT"))
    if "accountability_flag" not in existing_columns:
        columns_to_add.append(("accountability_flag", "INTEGER DEFAULT 0"))

    if not columns_to_add:
        print("\n[SKIP] keyword_group, accountability_flag 컬럼이 이미 존재함")
    else:
        for col_name, col_type in columns_to_add:
            sql = f"ALTER TABLE posts ADD COLUMN {col_name} {col_type}"
            print(f"\n[ALTER] {sql}")
            if not dry_run:
                cur.execute(sql)

    # ── keyword_group 업데이트 ─────────────────────────────────────────────────
    print("\n[UPDATE] keyword_group 매핑 중...")
    update_counts = {}
    for keyword, group in KEYWORD_GROUP_MAP.items():
        sql = "UPDATE posts SET keyword_group = ? WHERE keyword = ?"
        cur.execute("SELECT COUNT(*) FROM posts WHERE keyword = ?", (keyword,))
        cnt = cur.fetchone()[0]
        if cnt > 0:
            print(f"  [{group:10s}] '{keyword}' → {cnt}건")
            if not dry_run:
                cur.execute(sql, (group, keyword))
        update_counts[keyword] = cnt

    # 매핑 안 된 키워드 확인
    if not dry_run:
        cur.execute("""
            SELECT keyword, COUNT(*) as cnt
            FROM posts
            WHERE keyword_group IS NULL
            GROUP BY keyword
            ORDER BY cnt DESC
        """)
        unmapped = cur.fetchall()
        if unmapped:
            print(f"\n[경고] keyword_group 미매핑 키워드:")
            for kw, cnt in unmapped:
                print(f"  '{kw}': {cnt}건")
        else:
            print("\n[OK] 미매핑 키워드 없음")
    else:
        # dry-run: keyword_group 컬럼 미존재이므로 keyword 기반 역추론
        mapped_keywords = set(KEYWORD_GROUP_MAP.keys())
        cur.execute("""
            SELECT keyword, COUNT(*) as cnt
            FROM posts
            GROUP BY keyword
            ORDER BY cnt DESC
        """)
        all_kws = cur.fetchall()
        unmapped = [(kw, cnt) for kw, cnt in all_kws if kw not in mapped_keywords]
        if unmapped:
            print(f"\n[경고] keyword_group 미매핑 키워드:")
            for kw, cnt in unmapped:
                print(f"  '{kw}': {cnt}건")
        else:
            print("\n[OK] 미매핑 키워드 없음 (예상)")

    # ── accountability_flag 업데이트 ───────────────────────────────────────────
    print("\n[UPDATE] accountability_flag 설정 중...")
    for kw in ACCOUNTABILITY_KEYWORDS:
        cur.execute("SELECT COUNT(*) FROM posts WHERE keyword = ?", (kw,))
        cnt = cur.fetchone()[0]
        print(f"  '{kw}' → {cnt}건에 accountability_flag=1 설정")
        if not dry_run:
            cur.execute(
                "UPDATE posts SET accountability_flag = 1 WHERE keyword = ?",
                (kw,)
            )

    # ── 검증 ──────────────────────────────────────────────────────────────────
    print("\n[검증] 그룹별 최종 건수:")
    if not dry_run:
        cur.execute("""
            SELECT keyword_group, COUNT(*) as cnt
            FROM posts
            GROUP BY keyword_group
            ORDER BY cnt DESC
        """)
        for group, cnt in cur.fetchall():
            label = group if group else "NULL(미매핑)"
            print(f"  {label:12s}: {cnt}건")

        cur.execute("SELECT COUNT(*) FROM posts WHERE accountability_flag = 1")
        acc_cnt = cur.fetchone()[0]
        print(f"\n  accountability_flag=1: {acc_cnt}건")

        con.commit()
        print("\n[완료] 커밋 완료")
    else:
        print("  (dry-run: 실제 DB 변경 없음)")

    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=DEFAULT_DB, help="SQLite DB 경로")
    parser.add_argument("--dry-run", action="store_true", help="실제 변경 없이 미리 확인")
    args = parser.parse_args()
    main(args.db, args.dry_run)
