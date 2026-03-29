"""Central configuration — single source of truth for paths and keyword mappings."""

from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR     = PROJECT_ROOT / "data"
DB_PATH      = DATA_DIR / "processed" / "naver_posts.db"
CAVES_DIR    = DATA_DIR / "caves" / "processed"
OUTPUT_DIR   = DATA_DIR / "exports" / "labeled"
KAPPA_DIR    = DATA_DIR / "exports" / "kappa"

# ── Keyword → Group mapping ─────────────────────────────────────────────────

KEYWORD_GROUP_MAP: dict[str, str] = {
    # FM_Direct
    "코로나 백신 이물질": "FM_Direct",
    "감사원 백신":       "FM_Direct",
    "코로나 백신 곰팡이": "FM_Direct",
    "정은경 백신":       "FM_Direct",
    # Court
    "코로나 백신 소송":       "Court",
    "백신 심근경색 판결":     "Court",
    "코로나 백신 항소":       "Court",
    "질병청 항소":           "Court",
    "코백회":               "Court",
    "백신 피해 법원":        "Court",
    "코로나 백신 사망 판결":  "Court",
    # Chronic
    "코로나 백신 피해":     "Chronic",
    "백신 피해 보상":       "Chronic",
    "코로나 백신 부작용":   "Chronic",
    "백신 피해자 모임":     "Chronic",
    "코로나 백신 정부 책임": "Chronic",
}

# Keywords targeted by collect_all.py (subset used for Naver API collection)
COLLECT_KEYWORDS: list[str] = [
    "코로나 백신 이물질",
    "감사원 백신",
    "코로나 백신 곰팡이",
    "코로나 백신 피해",
    "백신 피해 보상",
    "코로나 백신 부작용",
    "백신 피해자 모임",
    "정은경 백신",
    "코로나 백신 정부 책임",
]
