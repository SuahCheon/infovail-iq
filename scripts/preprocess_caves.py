"""
CAVES → 7C 벤치마크용 전처리 스크립트

입력: caves-data/labelled_tweets/csv_labels/{train,val,test}.csv (Poddar et al. 2022 원본)
출력: data/caves/processed/{train,val,test}.csv (7C 매핑 적용, 정제 완료)

전처리 규칙:
  1. religious 단독 레이블 샘플 제외 (개념적 한계 + 표본 부족 64건)
  2. religious 복합 레이블 → religious 태그만 strip, 나머지 유지
  3. none 레이블 샘플 제외 (7C 매핑 대상 없음)
  4. CAVES→7C 레이블 변환 (Stage 1 매핑 테이블 기준)
  5. 원본 split(train/val/test) 유지 — reproducibility
"""

import pandas as pd
from pathlib import Path

# ── 경로 설정 ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "caves-data" / "labelled_tweets" / "csv_labels"
OUT_DIR = PROJECT_ROOT / "data" / "caves" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── CAVES→7C 매핑 테이블 (7C_CODEBOOK.md Section 5 기준) ──
CAVES_TO_7C = {
    "side-effect":  ["C1"],
    "ineffective":  ["C1"],
    "rushed":       ["C1", "C4"],
    "ingredients":  ["C1"],
    "pharma":       ["C1"],
    "conspiracy":   ["C7"],
    "political":    ["C1", "C7"],
    "mandatory":    ["C6"],
    "unnecessary":  ["C2"],
    "country":      ["C1"],
    # religious: 제외 (개념적 한계 + n=64)
}

C7_DIMS = ["C1", "C2", "C3", "C4", "C5", "C6", "C7"]


def caves_labels_to_7c(caves_str: str) -> dict[str, int]:
    """CAVES 레이블 문자열 → 7C 이진 벡터 딕셔너리."""
    result = {dim: 0 for dim in C7_DIMS}
    for label in caves_str.split():
        for dim in CAVES_TO_7C.get(label, []):
            result[dim] = 1
    return result


def preprocess_split(split: str) -> pd.DataFrame | None:
    """단일 split 전처리."""
    path = RAW_DIR / f"{split}.csv"
    if not path.exists():
        print(f"  [SKIP] {path} not found")
        return None

    df = pd.read_csv(path)
    n_orig = len(df)

    # 1. religious 단독 제외
    mask_religious_only = df["labels"].str.strip() == "religious"
    n_religious_only = mask_religious_only.sum()

    # 2. none 제외
    mask_none = df["labels"].str.strip() == "none"
    n_none = mask_none.sum()

    # 필터링
    df = df[~mask_religious_only & ~mask_none].copy()

    # 3. religious strip (복합 레이블에서 제거)
    df["caves_labels"] = (
        df["labels"]
        .str.replace(r"\breligious\b", "", regex=True)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)  # 다중 공백 정리
    )

    # 4. CAVES→7C 변환
    c7_records = df["caves_labels"].apply(caves_labels_to_7c)
    c7_df = pd.DataFrame(c7_records.tolist())
    df = pd.concat([df[["ID", "text", "caves_labels"]].reset_index(drop=True), c7_df], axis=1)

    # 저장
    out_path = OUT_DIR / f"{split}.csv"
    df.to_csv(out_path, index=False)

    print(f"  {split:10s}: {n_orig} → {len(df)} "
          f"(religious_only={n_religious_only}, none={n_none})")

    return df


def main():
    print("CAVES → 7C 전처리")
    print(f"  입력: {RAW_DIR}")
    print(f"  출력: {OUT_DIR}")
    print()

    all_dfs = []
    for split in ["train", "val", "test"]:
        df = preprocess_split(split)
        if df is not None:
            all_dfs.append(df)

    # combined도 생성
    if all_dfs:
        combined = pd.concat(all_dfs, ignore_index=True)
        combined.to_csv(OUT_DIR / "combined.csv", index=False)
        print(f"\n  combined : {len(combined)}건 저장")

    # 7C 분포 요약
    print("\n── 7C 레이블 분포 (combined) ──")
    for dim in C7_DIMS:
        cnt = combined[dim].sum()
        pct = cnt / len(combined) * 100
        print(f"  {dim}: {cnt:>5,}건 ({pct:5.1f}%)")


if __name__ == "__main__":
    main()
