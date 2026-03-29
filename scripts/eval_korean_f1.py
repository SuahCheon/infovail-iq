"""
eval_korean_f1.py
-----------------
Gold standard 50건 x LLM 분류 결과 교차검증 -> 한국어 F1 산출

post_id 컬럼이 gold xlsx에 없으면 --csv 인수로 sample CSV를 지정하여
sample_id 기준 병합 후 매칭한다.

Usage:
    python scripts/eval_korean_f1.py \
        --gold  data/exports/kappa/coding_sample_v2_20260323_194126_답변.xlsx \
        --pred  data/exports/labeled/naver_all_20260323_202551_batch.jsonl \
        --csv   data/exports/kappa/sample_50_20260323_194126.csv \
        --out   data/exports/kappa/korean_f1_results.json

    # all-zero 제외 버전
    python scripts/eval_korean_f1.py \
        --gold  data/exports/kappa/coding_sample_v2_20260323_194126_답변.xlsx \
        --pred  data/exports/labeled/naver_all_20260323_202551_batch.jsonl \
        --csv   data/exports/kappa/sample_50_20260323_194126.csv \
        --out   data/exports/kappa/korean_f1_results_excl_na.json \
        --exclude-allzero
"""

import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

DIMENSIONS = ["C1", "C2", "C4", "C6", "C7"]


def load_gold(gold_path: Path, csv_path: Path | None) -> pd.DataFrame:
    df = pd.read_excel(gold_path, sheet_name="코딩폼")

    # 컬럼명 정규화: "C1\n(Confidence)" -> "C1"
    col_map = {}
    for col in df.columns:
        for dim in DIMENSIONS:
            if col.startswith(dim):
                col_map[col] = dim
    df = df.rename(columns=col_map)

    # post_id 병합 (없으면 CSV에서)
    if "post_id" not in df.columns:
        if csv_path is None:
            raise ValueError(
                "Gold xlsx에 post_id 컬럼 없음. --csv 인수로 sample CSV 경로 지정 필요"
            )
        csv_df = pd.read_csv(csv_path, dtype={"post_id": str})
        print(f"post_id 병합: {csv_path.name} (sample_id 기준)")
        df = df.merge(csv_df[["sample_id", "post_id"]], on="sample_id", how="left")
        n_missing = df["post_id"].isna().sum()
        if n_missing:
            print(f"  경고: post_id 매칭 실패 {n_missing}건")

    df["post_id"] = df["post_id"].astype(str)
    return df[["post_id", "sample_id"] + DIMENSIONS]


def load_pred(path: Path) -> dict:
    pred = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            pid = str(r["post_id"])
            pred[pid] = {dim: r.get(f"pred_{dim}", -1) for dim in DIMENSIONS}
    return pred


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", required=True)
    parser.add_argument("--pred", required=True)
    parser.add_argument("--csv", default=None,
                        help="sample CSV (post_id 병합용, gold에 post_id 없을 때)")
    parser.add_argument("--out", default="data/exports/kappa/korean_f1_results.json")
    parser.add_argument("--exclude-allzero", action="store_true",
                        help="all-zero gold standard 케이스 제외")
    args = parser.parse_args()

    gold_df = load_gold(
        Path(args.gold),
        Path(args.csv) if args.csv else None
    )
    pred_map = load_pred(Path(args.pred))

    # post_id 기준 매칭
    matched, missing = [], []
    for _, row in gold_df.iterrows():
        pid = row["post_id"]
        if pid in pred_map:
            matched.append(row)
        else:
            missing.append(pid)

    if missing:
        print(f"LLM 결과에서 매칭 안 된 post_id: {len(missing)}건")
        print(f"   샘플: {missing[:5]}")

    matched_df = pd.DataFrame(matched)

    # all-zero 제외 옵션
    if args.exclude_allzero:
        all_zero_mask = (matched_df[DIMENSIONS].fillna(0) == 0).all(axis=1)
        n_excluded = all_zero_mask.sum()
        matched_df = matched_df[~all_zero_mask]
        print(f"all-zero {n_excluded}건 제외 -> 분석 대상 {len(matched_df)}건")

    print(f"\n분석 대상: {len(matched_df)}건 (전체 gold {len(gold_df)}건)")

    # 차원별 F1
    results = {}
    y_true_all, y_pred_all = [], []

    print(f"\n{'차원':<6} {'Precision':>10} {'Recall':>8} {'F1':>8} {'Support':>8}")
    print("-" * 46)

    for dim in DIMENSIONS:
        y_true = matched_df[dim].fillna(0).astype(int).tolist()
        y_pred = [max(0, pred_map[str(row["post_id"])][dim])
                  for _, row in matched_df.iterrows()]
        # parse_error(-1) -> 0 처리
        y_pred = [0 if v < 0 else v for v in y_pred]

        if sum(y_true) == 0:
            print(f"{dim:<6} {'N/A (no positive)':>36}")
            results[dim] = {"precision": None, "recall": None, "f1": None, "support": 0}
            continue

        p = precision_score(y_true, y_pred, zero_division=0)
        r = recall_score(y_true, y_pred, zero_division=0)
        f = f1_score(y_true, y_pred, zero_division=0)
        sup = sum(y_true)

        print(f"{dim:<6} {p:>10.3f} {r:>8.3f} {f:>8.3f} {sup:>8}")
        results[dim] = {"precision": round(p, 3), "recall": round(r, 3),
                        "f1": round(f, 3), "support": sup}

        y_true_all.extend(y_true)
        y_pred_all.extend(y_pred)

    # Macro F1 (support=0인 차원 제외)
    valid_dims = [d for d in DIMENSIONS if results[d]["f1"] is not None]
    macro_f1 = sum(results[d]["f1"] for d in valid_dims) / len(valid_dims) if valid_dims else 0
    print(f"\n{'Macro F1':.<30} {macro_f1:.3f}  ({len(valid_dims)}차원 평균)")

    # 결과 저장
    output = {
        "gold_file":        args.gold,
        "pred_file":        args.pred,
        "n_gold":           len(gold_df),
        "n_matched":        len(matched_df),
        "n_missing":        len(missing),
        "exclude_allzero":  args.exclude_allzero,
        "dimensions":       results,
        "macro_f1":         round(macro_f1, 3),
        "valid_dims":       valid_dims,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"\n결과 저장: {out_path}")


if __name__ == "__main__":
    main()
