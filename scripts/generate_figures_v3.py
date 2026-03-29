"""
Infovail-IQ PoC1 — Figure 2 & 3 생성 스크립트
기준: naver_all_20260328_181231_batch.jsonl + naver_posts.db
출력: 300dpi PNG (JMIR 투고용)

Figure 2: 3개 그룹 × 3기간 7C prevalence grouped bar chart (panel a/b/c)
Figure 3: Daily volume time-series (hesitancy + informational + political)

실행: python scripts/generate_figures_v3.py  (from C:\infovail-iq\)
"""

import json
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
import numpy as np
from pathlib import Path
from datetime import date

# ── 경로 설정 ──────────────────────────────────────────────────────────────
BASE = Path(__file__).parent.parent  # C:\infovail-iq
JSONL_PATH = BASE / "data/exports/labeled/naver_all_20260328_181231_batch.jsonl"
DB_PATH    = BASE / "data/processed/naver_posts.db"
OUT_DIR    = BASE / "outputs/figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── 이벤트 날짜 ────────────────────────────────────────────────────────────
E1 = date(2026, 2, 23)  # BAI audit disclosure
E2 = date(2026, 3, 2)   # SBS broadcast

# ── 색상 팔레트 (colorblind-safe Tableau 10) ───────────────────────────────
COLORS = {
    "Pre-E1":  "#4E79A7",
    "E1→E2":   "#F28E2B",
    "Post-E2": "#E15759",
}

# ── 1. 데이터 로드 ─────────────────────────────────────────────────────────
print("Loading JSONL...")
records = []
with open(JSONL_PATH, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            records.append(json.loads(line))
df_pred = pd.DataFrame(records)
print(f"  JSONL rows: {len(df_pred)}")

print("Loading DB...")
conn = sqlite3.connect(DB_PATH)
df_db = pd.read_sql("""
    SELECT post_id, published_at, channel, content_type, keyword_group
    FROM posts
    WHERE is_relevant = 1
""", conn)
conn.close()
print(f"  DB rows: {len(df_db)}")

# ── 2. 병합 (JSONL의 keyword_group 제거 후 merge — DB 기준 사용) ───────────
df = df_pred.drop(columns=["keyword_group"]).merge(
    df_db[["post_id", "published_at", "channel", "content_type", "keyword_group"]],
    on="post_id", how="inner"
)
print(f"  Merged rows: {len(df)}")

df["date"] = pd.to_datetime(df["published_at"]).dt.date

# ── 3. Period 분류 ─────────────────────────────────────────────────────────
def assign_period(d):
    if d < E1:
        return "Pre-E1"
    elif d <= E2:
        return "E1→E2"
    else:
        return "Post-E2"

df["period"] = df["date"].apply(assign_period)
PERIOD_ORDER = ["Pre-E1", "E1→E2", "Post-E2"]

# ── 4. Main corpus ─────────────────────────────────────────────────────────
df_main = df[df["content_type"].isin(["hesitancy", "informational"])].copy()
print(f"  Main corpus: {len(df_main)}")

for g in ["FM_Direct", "Court", "Chronic"]:
    n = len(df_main[df_main["keyword_group"] == g])
    print(f"    {g}: {n}")

# ── ════════════════════════════════════════════════════════════════════════
#    Figure 2: 3-panel 7C prevalence grouped bar chart
# ════════════════════════════════════════════════════════════════════════ ──
DIMS = ["C1", "C4", "C6", "C7"]
GROUPS = ["FM_Direct", "Court", "Chronic"]

group_n = {g: len(df_main[df_main["keyword_group"] == g]) for g in GROUPS}
GROUP_LABELS = {
    "FM_Direct": f"(a) FM_Direct\n(n={group_n['FM_Direct']:,})",
    "Court":     f"(b) Court\n(n={group_n['Court']:,})",
    "Chronic":   f"(c) Chronic\n(n={group_n['Chronic']:,})",
}

# 유의성 마커 (stats_recalculated_v4.txt 기준, Pre-E1 vs Post-E2)
SIG_MARKERS = {
    ("FM_Direct", "C1"): "*",
    ("FM_Direct", "C4"): "ns",
    ("FM_Direct", "C6"): "ns",
    ("FM_Direct", "C7"): "ns",
    ("Court",     "C1"): "***",
    ("Court",     "C4"): "ns",
    ("Court",     "C6"): "ns",
    ("Court",     "C7"): "***",
    ("Chronic",   "C1"): "***",
    ("Chronic",   "C4"): "**",
    ("Chronic",   "C6"): "*",
    ("Chronic",   "C7"): "ns",
}

fig2, axes = plt.subplots(1, 3, figsize=(14, 5.8), sharey=False)
fig2.suptitle(
    "Figure 2. 7C-Type Prevalence by Discourse Group and Temporal Period",
    fontsize=12, fontweight="bold", y=1.02
)

x = np.arange(len(DIMS))
width = 0.22
offsets = [-width, 0, width]

for ax, group in zip(axes, GROUPS):
    gdf = df_main[df_main["keyword_group"] == group]

    bar_tops = {}

    for i, (period, offset) in enumerate(zip(PERIOD_ORDER, offsets)):
        pdf = gdf[gdf["period"] == period]
        n = len(pdf)
        vals = []
        for d in DIMS:
            col = f"pred_{d}"
            v = pdf[col].mean() * 100 if n > 0 else 0
            vals.append(v)
        bar_tops[period] = vals

        bars = ax.bar(
            x + offset, vals, width,
            label=f"{period} (n={n:,})",
            color=COLORS[period],
            alpha=0.88, edgecolor="white", linewidth=0.5
        )

        # 값 레이블 (10% 이상만)
        for bar, val in zip(bars, vals):
            if val >= 10:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 1.0,
                    f"{val:.0f}",
                    ha="center", va="bottom", fontsize=6.5, color="#333"
                )

    # 유의성 브라켓 (Pre-E1 vs Post-E2)
    for di, dim in enumerate(DIMS):
        marker = SIG_MARKERS.get((group, dim), "")
        if marker and marker != "ns":
            pre_val  = bar_tops["Pre-E1"][di]
            post_val = bar_tops["Post-E2"][di]
            ymax = max(pre_val, post_val) + 7
            x1 = di + offsets[0]
            x2 = di + offsets[2]
            ax.plot([x1, x1, x2, x2],
                    [ymax, ymax+2, ymax+2, ymax],
                    lw=0.9, color="#333")
            ax.text((x1+x2)/2, ymax+2.5, marker,
                    ha="center", va="bottom", fontsize=8, color="#111")

    ax.set_title(GROUP_LABELS[group], fontsize=10, fontweight="bold", pad=8)
    ax.set_xticks(x)
    ax.set_xticklabels(["C1\nConfidence", "C4\nCalculation",
                         "C6\nCompliance", "C7\nConspiracy"], fontsize=8.5)
    ax.set_ylim(0, 115)
    ax.set_ylabel("Prevalence (%)" if group == "FM_Direct" else "", fontsize=9)
    ax.yaxis.set_tick_params(labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, linestyle=":", alpha=0.4, zorder=0)
    ax.set_axisbelow(True)

# 공통 범례
handles = [mpatches.Patch(color=COLORS[p], alpha=0.88, label=p) for p in PERIOD_ORDER]
fig2.legend(handles=handles, loc="lower center", ncol=3,
            fontsize=9, frameon=False, bbox_to_anchor=(0.5, -0.04))

fig2.text(
    0.5, -0.10,
    "E1 = BAI audit disclosure (February 23, 2026); "
    "E2 = SBS broadcast on court-recognized COVID-19 vaccination–related myocardial infarction death (March 2, 2026).\n"
    "C2 Complacency omitted (prevalence <1% across all groups). "
    "Significance brackets: Pre-E1 vs Post-E2 (Fisher's exact test). "
    "*p<0.05, **p<0.01, ***p<0.001.",
    ha="center", fontsize=7.5, color="#444", style="italic"
)

plt.tight_layout(rect=[0, 0.05, 1, 1])
out2 = OUT_DIR / "figure2_7C_prevalence_v3.png"
fig2.savefig(out2, dpi=300, bbox_inches="tight", facecolor="white")
print(f"\n✅ Figure 2 saved: {out2}")
plt.close()


# ── ════════════════════════════════════════════════════════════════════════
#    Figure 3: Daily volume time-series
# ════════════════════════════════════════════════════════════════════════ ──
conn = sqlite3.connect(DB_PATH)
df_all = pd.read_sql("""
    SELECT published_at, content_type
    FROM posts
    WHERE published_at IS NOT NULL
""", conn)
conn.close()

df_all["date"] = pd.to_datetime(df_all["published_at"]).dt.date
start_dt = date(2026, 2, 7)
end_dt   = date(2026, 3, 21)
df_all = df_all[(df_all["date"] >= start_dt) & (df_all["date"] <= end_dt)]

daily = df_all.groupby(["date", "content_type"]).size().unstack(fill_value=0)

for ct in ["hesitancy", "informational", "political", "irrelevant", "pro_vaccine"]:
    if ct not in daily.columns:
        daily[ct] = 0

all_dates = pd.date_range(start_dt, end_dt).date
daily = daily.reindex(all_dates, fill_value=0)
daily.index = pd.to_datetime(daily.index)

# Legend n값: stats_recalculated_v4.txt 확정값 (published_at 없는 소수 건 제외 보정)
n_hes  = 2671
n_info = 339
n_pol  = 1409

fig3, ax = plt.subplots(figsize=(12, 4.8))

ax.fill_between(daily.index, daily["hesitancy"],
                color="#4E79A7", alpha=0.78,
                label=f"Hesitancy (n={n_hes:,})")
ax.fill_between(daily.index, daily["informational"],
                color="#59A14F", alpha=0.78,
                label=f"Informational (n={n_info:,})")
ax.fill_between(daily.index, daily["political"],
                color="#F28E2B", alpha=0.55,
                label=f"Political — excl. from primary analysis (n={n_pol:,})")

y_max = max(
    daily["hesitancy"].max(),
    daily["informational"].max(),
    daily["political"].max()
) * 1.30

ax.set_ylim(0, y_max)

for ev_date_raw, ev_label, ev_color in [
    (E1, "E1 (Feb 23)", "#E15759"),
    (E2, "E2 (Mar 2)",  "#B07AA1"),
]:
    ev_dt = pd.Timestamp(ev_date_raw)
    ax.axvline(ev_dt, color=ev_color, linewidth=1.8, linestyle="--", alpha=0.85)
    ax.text(ev_dt, y_max * 0.93, ev_label,
            color=ev_color, fontsize=8.5, ha="center", va="top",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                      edgecolor=ev_color, alpha=0.9, linewidth=0.8))

# Peak 주석
for pk_date, col_name in [
    (date(2026, 2, 24), "hesitancy"),
    (date(2026, 3,  3), "hesitancy"),
]:
    pk_ts  = pd.Timestamp(pk_date)
    pk_val = int(daily.loc[pk_ts, col_name])
    ax.annotate(
        f"{pk_ts.strftime('%b %d')}\n(n={pk_val})",
        xy=(pk_ts, pk_val),
        xytext=(pk_ts, pk_val + y_max * 0.10),
        fontsize=7.5, ha="center", color="#1A1A1A",
        arrowprops=dict(arrowstyle="->", color="#555", lw=0.8)
    )

ax.set_title(
    "Figure 3. Daily Post Volume by Content Type\n"
    "(Naver Blog + News Comment, February 7 – March 21, 2026)",
    fontsize=11, fontweight="bold", pad=10
)
ax.set_xlabel("Date", fontsize=9)
ax.set_ylabel("Daily Posts (n)", fontsize=9)
ax.set_xlim(pd.Timestamp(start_dt), pd.Timestamp(end_dt))

ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right", fontsize=8)

ax.legend(loc="upper right", fontsize=8.5, frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, linestyle=":", alpha=0.35, zorder=0)
ax.set_axisbelow(True)

fig3.text(
    0.5, -0.04,
    "E1 = BAI audit disclosure (February 23, 2026); "
    "E2 = SBS broadcast on court-recognized COVID-19 vaccination–related myocardial infarction death (March 2, 2026).\n"
    "Political posts (n=1,409) excluded from primary hesitancy analysis; displayed here for contextual comparison. "
    "Peak hesitancy volume: February 24 (n=313), March 3 (n=306).",
    ha="center", fontsize=7.5, color="#444", style="italic"
)

plt.tight_layout()
out3 = OUT_DIR / "figure3_daily_volume_v3.png"
fig3.savefig(out3, dpi=300, bbox_inches="tight", facecolor="white")
print(f"✅ Figure 3 saved: {out3}")
plt.close()

print("\n── Summary ────────────────────────────────────────────")
print(f"  Figure 2: {out2}")
print(f"  Figure 3: {out3}")
print("────────────────────────────────────────────────────────")
