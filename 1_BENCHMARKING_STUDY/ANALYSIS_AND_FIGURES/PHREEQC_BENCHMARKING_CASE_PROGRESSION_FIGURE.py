"""
Companion to PHREEQC_BENCHMARKING_COMBINED_FIGURE.py.

Where the combined figure shows one CASE per panel (with three days
overlaid), this figure re-groups the data: one DAY per panel, with all
three cases (no reaction / decay / decay + production) overlaid. Reader
sees how the simulated and analytical profiles shift as decay (Case 1 ->
Case 2) and production (Case 2 -> Case 3) are added at each time
snapshot.

Reuses the same input workbook
(RESULTS_BENCHMARKING_ANALYTICAL_SOLUTION_750CM.xlsx) and the same Wong
palette + marker family the day-grouped figure uses; here colour and
marker shape encode CASE rather than DAY.

Saves PNG (300 + 600 DPI), PDF, SVG, EPS to FIGURES/ alongside the
existing benchmarking figure.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

XLSX_FILE = "RESULTS_BENCHMARKING_ANALYTICAL_SOLUTION_750CM.xlsx"
SHEETS = ["CASE_1", "CASE_2", "CASE_3"]
DAYS = [1, 2, 3]
DAY_PANEL_TITLES = ["(a) Day 1", "(b) Day 2", "(c) Day 3"]
N_VIS = 50

# Wong (2011) colourblind-safe palette mapped to CASES (matches the
# day-grouped figures' Day 1 / 2 / 3 ordering, so the same colour and
# marker shape pick up the same index across figures even though the
# encoded variable changes).
CASE_COLORS = {1: "#0072B2", 2: "#009E73", 3: "#D55E00"}
CASE_MARKERS = {1: "s", 2: "^", 3: "D"}


def panel(ax, sheets, day, panel_title):
    """Draw one day's panel: three cases overlaid (sim lines + analytical scatter)."""
    # Simulated dashed lines first so the legend ordering is sim-row, scatter-row.
    for case_idx, sheet_name in enumerate(SHEETS, start=1):
        sub = sheets[sheet_name]
        sub = sub[sub["DAY"] == day].sort_values("Y").reset_index(drop=True)
        if sub.empty:
            continue
        ax.plot(sub["CONC_RATIO_SIMULATED"], sub["Y"],
                zorder=1, linestyle="--", color=CASE_COLORS[case_idx],
                label=f"Simulated (Scenario {case_idx})")

    for case_idx, sheet_name in enumerate(SHEETS, start=1):
        sub = sheets[sheet_name]
        sub = sub[sub["DAY"] == day].sort_values("Y").reset_index(drop=True)
        ana_col = f"CONC_RATIO_ANALYTICAL_AT_Y_DAY_{day}"
        if sub.empty or ana_col not in sub.columns:
            continue
        n = min(N_VIS, len(sub))
        idx = np.linspace(0, len(sub) - 1, n, dtype=int)
        ax.scatter(sub.iloc[idx][ana_col], sub.iloc[idx]["Y"],
                   zorder=2, color=CASE_COLORS[case_idx],
                   edgecolor="black", s=20,
                   marker=CASE_MARKERS[case_idx],
                   label=f"Analytical (Scenario {case_idx})")

    ax.set_xlabel("Concentration (mols/l)", fontsize=24, labelpad=10)
    ax.set_xlim(-0.001, 1.0)
    ax.set_ylim(0, 750)
    ax.set_yticks([0, 100, 200, 300, 400, 500, 600, 700, 750])
    ax.set_clip_on(True)
    ax.set_title(panel_title, fontsize=24, weight="bold")
    ax.grid(True, color="gray", alpha=0.3, linewidth=0.5)
    ax.minorticks_on()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    xlsx_path = os.path.join(here, XLSX_FILE)
    sheets = {s: pd.read_excel(xlsx_path, sheet_name=s) for s in SHEETS}
    for s, df in sheets.items():
        missing = [f"CONC_RATIO_ANALYTICAL_AT_Y_DAY_{t}" for t in DAYS
                   if f"CONC_RATIO_ANALYTICAL_AT_Y_DAY_{t}" not in df.columns]
        if missing:
            raise RuntimeError(
                f"Sheet '{s}' is missing analytical-at-Y columns: {missing}. "
                f"Run ANALYTICAL_AT_SIMULATED_DEPTHS_CASE_{{1,2,3}}.py first."
            )

    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman", "DejaVu Serif"]
    plt.rcParams["mathtext.fontset"] = "stix"
    plt.rcParams["axes.unicode_minus"] = False
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(19.2, 11.9))

    for ax, day, ptitle in zip(axes, DAYS, DAY_PANEL_TITLES):
        panel(ax, sheets, day, ptitle)

    axes[0].set_ylabel("Height above the column base (cm)", fontsize=24)
    axes[0].tick_params(axis="both", labelsize=22, pad=10)
    axes[1].tick_params(axis="x", labelsize=22, pad=10)
    axes[1].tick_params(axis="y", labelleft=False, direction="in")
    axes[2].tick_params(axis="x", labelsize=22, pad=10)
    axes[2].tick_params(axis="y", direction="in", labelleft=False,
                        labelright=True, labelsize=22, pad=10)
    axes[2].tick_params(right=True, direction="out")

    fig.tight_layout()

    handles, labels = axes[0].get_legend_handles_labels()
    n = len(SHEETS)
    interleaved_h, interleaved_l = [], []
    for i in range(n):
        interleaved_h.extend([handles[i], handles[i + n]])
        interleaved_l.extend([labels[i], labels[i + n]])
    fig.subplots_adjust(bottom=0.26)
    fig.legend(interleaved_h, interleaved_l, loc="lower center", ncol=n,
               fontsize=24, frameon=True, framealpha=1.0, markerscale=2.0,
               bbox_to_anchor=(0.5, 0.01))

    figures_dir = os.path.join(here, "FIGURES")
    os.makedirs(figures_dir, exist_ok=True)
    base = "PHREEQC_Benchmarking_CASE_PROGRESSION_BY_DAY"
    out_300 = os.path.join(figures_dir, f"{base}_300DPI.png")
    out_600 = os.path.join(figures_dir, f"{base}_600DPI.png")
    out_pdf = os.path.join(figures_dir, f"{base}_Vector.pdf")
    out_svg = os.path.join(figures_dir, f"{base}_Vector.svg")
    out_eps = os.path.join(figures_dir, f"{base}_Vector.eps")

    fig.savefig(out_300, dpi=300, bbox_inches="tight",
                facecolor="white", edgecolor="none", format="png")
    fig.savefig(out_600, dpi=600, format="png")
    fig.savefig(out_pdf, bbox_inches="tight",
                facecolor="white", edgecolor="none", format="pdf")
    fig.savefig(out_svg, bbox_inches="tight",
                facecolor="white", edgecolor="none", format="svg")
    fig.savefig(out_eps, bbox_inches="tight",
                facecolor="white", edgecolor="none", format="eps")

    for p in [out_300, out_600, out_pdf, out_svg, out_eps]:
        print(f"Saved: {p}")
    plt.show()


if __name__ == "__main__":
    main()
