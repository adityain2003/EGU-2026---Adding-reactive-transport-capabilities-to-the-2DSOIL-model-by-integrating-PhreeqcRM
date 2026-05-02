"""
Process-decomposition figure for the benchmarking study (Option C).

Each panel (one per day) decomposes the simulated profile into:
  - Transport baseline:  C(Case 1)                 (reaches 0..1)
  - Decay effect:        C(Case 2) - C(Case 1)     (typically <= 0)
  - Production effect:   C(Case 3) - C(Case 2)     (typically >= 0)

The three contributions sum to C(Case 3) at every depth. Plotting them
together on a common x-axis (with a vertical reference line at zero)
shows the relative magnitude of transport vs the reactive corrections.

Companion to PHREEQC_BENCHMARKING_CASE_PROGRESSION_FIGURE.py (Option A)
and PHREEQC_BENCHMARKING_DIFFERENCE_PROFILES_FIGURE.py (Option B).

Saves PNG (300 + 600 DPI), PDF, SVG, EPS to FIGURES/.
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

TRACE_DEFS = [
    {"label": "Scenario 2 (decay) - Scenario 1 (no reaction)",
     "kind": "delta", "minuend": "CASE_2", "subtrahend": "CASE_1",
     "color": "#009E73", "marker": "^"},
    {"label": "Scenario 3 (decay + production) - Scenario 2 (decay)",
     "kind": "delta", "minuend": "CASE_3", "subtrahend": "CASE_2",
     "color": "#D55E00", "marker": "D"},
]


def get_sim_for_day(sheet_df, day):
    sub = sheet_df[sheet_df["DAY"] == day].sort_values("Y").reset_index(drop=True)
    return sub["Y"].to_numpy(), sub["CONC_RATIO_SIMULATED"].to_numpy()


def get_analytical_for_day(sheet_df, day):
    ana_col = f"CONC_RATIO_ANALYTICAL_AT_Y_DAY_{day}"
    sub = sheet_df[sheet_df["DAY"] == 1].sort_values("Y").reset_index(drop=True)
    return sub["Y"].to_numpy(), sub[ana_col].to_numpy()


def trace_data(sheets, trace, day, kind):
    """Return (Y, x_values) for one trace; kind is 'sim' or 'ana'."""
    fetch = get_sim_for_day if kind == "sim" else get_analytical_for_day
    if trace["kind"] == "raw":
        return fetch(sheets[trace["sheet"]], day)
    m_y, m_v = fetch(sheets[trace["minuend"]], day)
    s_y, s_v = fetch(sheets[trace["subtrahend"]], day)
    if not np.array_equal(m_y, s_y):
        s_v = np.interp(m_y, s_y, s_v)
    return m_y, m_v - s_v


def panel(ax, sheets, day, panel_title):
    # Only the simulated differences are physically meaningful here: the
    # analytical solutions are derived for specific scenarios, not for
    # differences between scenarios, so subtracting two analytical curves
    # would not correspond to any closed-form solution.
    for trace in TRACE_DEFS:
        y, x = trace_data(sheets, trace, day, "sim")
        ax.fill_betweenx(y, 0, x, color=trace["color"], alpha=0.18, zorder=0)
        ax.plot(x, y, zorder=1, linestyle="--", color=trace["color"],
                label=trace["label"])

    ax.axvline(x=0, color="black", linewidth=0.8, zorder=0)
    ax.set_xlabel(r"$\Delta$Concentration (mols/l)",
                  fontsize=24, labelpad=10)
    ax.set_xlim(-0.3, 0.3)
    ax.set_xticks([-0.3, -0.15, 0, 0.15, 0.3])
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
    fig.subplots_adjust(bottom=0.20, wspace=0.18)
    fig.legend(handles, labels, loc="lower center", ncol=len(TRACE_DEFS),
               fontsize=22, frameon=True, framealpha=1.0, markerscale=2.0,
               bbox_to_anchor=(0.5, 0.01))

    figures_dir = os.path.join(here, "FIGURES")
    os.makedirs(figures_dir, exist_ok=True)
    base = "PHREEQC_Benchmarking_DECOMPOSITION_BY_DAY"
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
