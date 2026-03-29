"""
collect_retrospective.py
------------------------
전체 관측 기간(2026-02-07 ~ 2026-03-21) 소급 수집

- Naver API는 날짜 필터 미지원 -> 최신순 최대 1,000건 수집 후 날짜 필터
- 기존 DB의 post_id와 중복 체크 -> 신규 포스트만 INSERT
- DB 스키마: post_id, channel, content, author_hash, published_at,
             keyword, collected_at, keyword_group, accountability_flag, is_relevant
- post_id = sha256(channel|date|content)[:16]  (기존 preprocessor.py 방식 일치)

Usage:
    python scripts/collect_retrospective.py --dry-run   # DB 저장 없이 건수만 확인
    python scripts/collect_retrospective.py             # 실제 수집
"""

import os, time, sqlite3, hashlib, html, re, argparse
from datetime import date, datetime
from pathlib import Path
import httpx
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID     = os.getenv("NAVER_CLIENT_ID")
CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
DB_PATH       = Path("data/processed/naver_posts.db")

DATE_START = date(2026, 2, 7)
DATE_END   = date(2026, 3, 21)

KEYWORDS = {
    "FM_Direct": [
        "백신 부작용", "코로나 백신", "백신 이상반응", "mRNA 백신",
        "화이자 부작용", "모더나 부작용", "백신 피해",
        "백신 사망", "백신 후유증", "아나필락시스",
    ],
    "Court": [
        "백신 소송", "백신 보상", "예방접종 피해", "심근염 백신",
        "백신 국가배상", "백신 판결", "백신 승소",
    ],
    "Chronic": [
        "질병관리청 백신", "백신 불신", "백신 거부",
    ],
}

CHANNELS = ["blog", "news"]
HEADERS  = {
    "X-Naver-Client-Id":     CLIENT_ID,
    "X-Naver-Client-Secret": CLIENT_SECRET,
}

_RE_HTML_TAG = re.compile(r"<[^>]+>")


def strip_html(text: str) -> str:
    return html.unescape(_RE_HTML_TAG.sub("", text))


def make_post_id(channel: str, content: str, pub_date_str: str) -> str:
    """Match preprocessor._make_post_id logic: sha256(channel|date|content)[:16]"""
    payload = f"{channel}|{pub_date_str}|{content}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def hash_author(nickname: str) -> str:
    if not nickname:
        return hashlib.sha256(b"__anonymous__").hexdigest()
    return hashlib.sha256(nickname.encode("utf-8")).hexdigest()


def parse_date(date_str: str):
    """'Mon, 24 Feb 2026 ...' 또는 'YYYYMMDD' 또는 'YYYY-MM-DD' 형식 파싱."""
    import email.utils
    try:
        return email.utils.parsedate_to_datetime(date_str).date()
    except Exception:
        pass
    try:
        return date.fromisoformat(date_str[:10])
    except Exception:
        pass
    try:
        # YYYYMMDD format (blog postdate)
        return date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:8]))
    except Exception:
        return None


def fetch_items(keyword: str, channel: str, max_items: int = 1000) -> list[dict]:
    items = []
    display = 10
    for start in range(1, max_items + 1, display):
        url = f"https://openapi.naver.com/v1/search/{channel}.json"
        params = {
            "query":   keyword,
            "display": display,
            "start":   start,
            "sort":    "date",
        }
        try:
            r = httpx.get(url, headers=HEADERS, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()
            batch = data.get("items", [])
            if not batch:
                break
            items.extend(batch)
            # 가장 오래된 포스트가 DATE_START보다 이전이면 중단
            oldest = batch[-1]
            pub = parse_date(oldest.get("postdate") or oldest.get("pubDate", ""))
            if pub and pub < DATE_START:
                break
            time.sleep(0.12)
        except Exception as e:
            print(f"  ERR {keyword}/{channel} start={start}: {e}")
            break
    return items


def filter_by_date(items: list[dict]) -> list[dict]:
    result = []
    for item in items:
        pub = parse_date(item.get("postdate") or item.get("pubDate", ""))
        if pub and DATE_START <= pub <= DATE_END:
            item["_parsed_date"] = pub
            result.append(item)
    return result


def get_existing_ids(con) -> set:
    rows = con.execute("SELECT post_id FROM posts").fetchall()
    return {r[0] for r in rows}


def process_and_insert(con, items: list[dict], keyword: str, group: str,
                       channel_type: str, existing_ids: set, dry_run: bool) -> int:
    new_count = 0
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for item in items:
        title = strip_html(item.get("title", ""))
        desc  = strip_html(item.get("description", ""))
        content = f"{title}\n{desc}".strip()

        pub = item.get("_parsed_date")
        pub_str = str(pub) if pub else None
        date_for_id = pub.strftime("%Y%m%d") if pub else "nodate"

        # channel mapping: blog API -> "blog", news API -> "news"
        channel = channel_type

        pid = make_post_id(channel, content, date_for_id)
        if pid in existing_ids:
            continue

        nickname = item.get("bloggername") or item.get("cafeName") or ""
        author_h = hash_author(nickname)

        if not dry_run:
            con.execute("""
                INSERT OR IGNORE INTO posts
                    (post_id, channel, content, author_hash, published_at,
                     keyword, collected_at, keyword_group, accountability_flag, is_relevant)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0)
            """, (pid, channel, content, author_h, pub_str,
                  keyword, now_str, group))

        existing_ids.add(pid)
        new_count += 1

    if not dry_run:
        con.commit()
    return new_count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="DB 저장 없이 건수만 출력")
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN 모드 - DB 저장 없음 ===\n")

    con = sqlite3.connect(DB_PATH)
    existing_ids = get_existing_ids(con)
    print(f"기존 DB: {len(existing_ids)}건\n")

    total_new = 0
    group_new = {}

    for group, keywords in KEYWORDS.items():
        group_new[group] = 0
        for keyword in keywords:
            for channel in CHANNELS:
                print(f"[{group}] '{keyword}' / {channel} ...", end=" ", flush=True)
                raw   = fetch_items(keyword, channel)
                filt  = filter_by_date(raw)
                new_n = process_and_insert(
                    con, filt, keyword, group, channel,
                    existing_ids, args.dry_run
                )
                print(f"수집 {len(raw)} -> 기간내 {len(filt)} -> 신규 {new_n}")
                total_new += new_n
                group_new[group] += new_n

    con.close()

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}총 신규 포스트: {total_new}건")
    for g, n in group_new.items():
        print(f"  {g}: {n}건")

    if not args.dry_run and total_new > 0:
        print("\n-> 다음 단계: filter_posts.py 재실행 + LLM 재분류")


if __name__ == "__main__":
    main()
