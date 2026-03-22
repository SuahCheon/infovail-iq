"""
plot_timeline.py  v2 -- 3그룹

그룹:
  FM_Direct : 이물질 직접 (감사원 이벤트)
  Court     : 법원판결   (SBS 이벤트)
  Chronic   : 만성 기저불신 (증폭기)
출력: outputs/figures/fig1_timeline.png (300 dpi)
"""

import sqlite3
from pathlib import Path
from datetime import date, timedelta
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

DB_PATH = Path("data/processed/naver_posts.db")
OUT_DIR = Path("outputs/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

GROUPS = {
    "FM_Direct": [
        "코로나 백신 이물질",
        "코로나 백신 곰팡이",
        "감사원 백신",
        "정은경 백신",          # accountability subtype
    ],
    "Court": [
        "코로나 백신 소송",
        "백신 심근경색 판결",
        "코로나 백신 항소",
        "질병청 항소",
        "코백회",
        "백신 피해 법원",
        "코로나 백신 사망 판결",
    ],
    "Chronic": [
        "코로나 백신 피해",
        "백신 피해 보상",
        "코로나 백신 부작용",
        "백신 피해자 모임",
        "코로나 백신 정부 책임",
        "백신 피해자",
    ],
}

STYLE = {
    "FM_Direct": dict(color="steelblue",  lw=2.2, ls="-",  alpha=0.9,
                      label="Foreign Matter Discourse (이물질/감사원)"),
    "Court":     dict(color="coral",      lw=2.2, ls="-",  alpha=0.9,
                      label="Court Ruling Discourse (판결/항소/코백회)"),
    "Chronic":   dict(color="dimgray",    lw=1.6, ls="--", alpha=0.7,
                      label="Chronic Distrust Discourse (부작용/피해/보상)"),
}

EVENTS = [
    ("2026-02-23", "Audit Disclosure\n(Feb 23)",      "firebrick"),
    ("2026-03-02", "SBS Report\n(Mar 2)",              "darkorange"),
    ("2026-03-04", "Advocacy\nPress Conf. (Mar 4)",    "goldenrod"),
]

START = date(2026, 2, 7)
END   = date(2026, 3, 21)


def get_daily(conn, keywords):
    ph = ",".join("?" * len(keywords))
    rows = conn.execute(f"""
        SELECT date(published_at), COUNT(*)
        FROM posts WHERE keyword IN ({ph})
        GROUP BY date(published_at)
    """, keywords).fetchall()
    return {r[0]: r[1] for r in rows}


def date_range(start, end):
    d = start
    while d <= end:
        yield d.isoformat()
        d += timedelta(days=1)


def main():
    conn = sqlite3.connect(DB_PATH)
    daily = {name: get_daily(conn, kws) for name, kws in GROUPS.items()}
    conn.close()

    dates = list(date_range(START, END))

    fig, ax = plt.subplots(figsize=(14, 5.5))

    for name, style in STYLE.items():
        vals = [daily[name].get(d, 0) for d in dates]
        ax.fill_between(dates, vals, alpha=0.08, color=style["color"])
        ax.plot(dates, vals, **style)

    # 이벤트 수직선
    y_max = ax.get_ylim()[1]
    for ev_date, label, color in EVENTS:
        if ev_date in dates:
            ax.axvline(x=ev_date, color=color, lw=1.6, ls="--", alpha=0.85)
            ax.text(ev_date, y_max * 0.97, label,
                    color=color, fontsize=8, ha="center", va="top",
                    bbox=dict(boxstyle="round,pad=0.25", fc="white",
                              ec=color, alpha=0.8))

    # Baseline / Post-event 영역
    ax.axvspan(dates[0], "2026-02-22", alpha=0.04, color="gray")
    ax.axvspan("2026-02-23", dates[-1], alpha=0.04, color="lightyellow")

    all_vals = [daily[n].get(d, 0) for n in GROUPS for d in dates]
    y_top = max(all_vals) * 1.05
    ax.text("2026-02-10", y_top * 0.78, "Baseline",
            fontsize=9, color="gray", alpha=0.8, ha="center")
    ax.text("2026-03-08", y_top * 0.78, "Post-event",
            fontsize=9, color="darkgoldenrod", alpha=0.8, ha="center")

    # x축 눈금
    key_dates = [
        "2026-02-07", "2026-02-14", "2026-02-21",
        "2026-02-23", "2026-03-02", "2026-03-04",
        "2026-03-07", "2026-03-14", "2026-03-21",
    ]
    ax.set_xticks([d for d in key_dates if d in dates])
    ax.set_xticklabels(
        [d[5:] for d in key_dates if d in dates],
        rotation=30, ha="right", fontsize=9
    )

    ax.set_xlabel("Date (2026)", fontsize=11)
    ax.set_ylabel("Number of Posts", fontsize=11)
    ax.set_title(
        "Daily Post Volume by Discourse Group\n"
        "Naver Blog + News Comments  |  Feb 7 - Mar 21, 2026  "
        "|  N = 5,973",
        fontsize=12, fontweight="bold"
    )
    ax.legend(loc="upper left", fontsize=9, framealpha=0.9)
    ax.grid(axis="y", ls=":", alpha=0.45)
    ax.set_xlim(dates[0], dates[-1])
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    out_path = OUT_DIR / "fig1_timeline.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[OK] saved: {out_path}")
    print(f"     FM={sum(daily['FM_Direct'].values())} "
          f"Court={sum(daily['Court'].values())} "
          f"Chronic={sum(daily['Chronic'].values())}")


if __name__ == "__main__":
    main()
