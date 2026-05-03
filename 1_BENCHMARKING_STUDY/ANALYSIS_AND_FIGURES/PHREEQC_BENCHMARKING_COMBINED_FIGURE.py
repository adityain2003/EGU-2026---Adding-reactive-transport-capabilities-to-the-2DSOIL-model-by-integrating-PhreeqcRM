"""
Combined 3-panel benchmarking figure replicating the layout of
1_PHREEQC_BENCHMARKING_STUDY_1_ANALYTICAL_SOLUTION/3_PHREEQC_2DSOIL_BENCHMARKING_COMPARATIVE_CURVES.py
(panels (a) CASE_1, (b) CASE_2, (c) CASE_3), but with the analytical
scatter sourced from the new CONC_RATIO_ANALYTICAL_AT_Y_DAY_k columns
(evaluated on the dense 437-node simulated grid, then subsampled to
50 markers per day for visual clarity).

Saves PNG (300 + 600 DPI), PDF, SVG, EPS - same outputs as the original
combined figure script.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import patheffects

XLSX_FILE = "RESULTS_BENCHMARKING_ANALYTICAL_SOLUTION_750CM.xlsx"
SHEETS = ["CASE_1", "CASE_2", "CASE_3"]
PANELS = [
    "No reaction",
    "Decay",
    "Decay + production",
]
PANEL_LABELS = ["(a)", "(b)", "(c)"]
PANEL_RATES = [
    ["μ = 0 s⁻¹", "γ = 0 s⁻¹"],                               # (a) no reaction
    ["μ = 3 × 10⁻⁶ s⁻¹", "γ = 0 s⁻¹"],                        # (b) decay only
    ["μ = 3 × 10⁻⁶ s⁻¹", "γ = 1 × 10⁻⁶ s⁻¹"],                 # (c) decay + production
]
DAYS = [1, 2, 3]   # DAY 0 omitted: trivial zero initial condition
# Wong (2011) colorblind-safe palette: blue, bluish green, vermillion.
DAY_COLORS = {1: "#0072B2", 2: "#009E73", 3: "#D55E00"}
DAY_MARKERS = {1: "s", 2: "^", 3: "D"}
N_VIS = 50


def panel(ax, df, title, label, rates):
    """Draw one Figure_1-style panel into ax."""
    one_day = df[df["DAY"] == 1].sort_values("Y").reset_index(drop=True)
    vis_idx = np.linspace(0, len(one_day) - 1, N_VIS, dtype=int)
    analytical_vis = one_day.iloc[vis_idx]

    for t in DAYS:
        sub = df[df["DAY"] == t].sort_values("Y")
        ax.plot(sub["CONC_RATIO_SIMULATED"], sub["Y"],
                zorder=1, linestyle="--", color=DAY_COLORS[t],
                label=f"Simulated (Day {t})")

    for t in DAYS:
        col = f"CONC_RATIO_ANALYTICAL_AT_Y_DAY_{t}"
        ax.scatter(analytical_vis[col], analytical_vis["Y"],
                   zorder=2, color=DAY_COLORS[t], edgecolor="black", s=20,
                   marker=DAY_MARKERS[t],
                   label=f"Analytical (Day {t})")

    ax.set_xlabel("Concentration (mols/l)", fontsize=24, labelpad=10)
    ax.set_xlim(-0.001, 1.0)
    ax.set_xticks([0.0, 0.5, 1.0])
    ax.set_xticklabels(["0.0", "0.5", "1.0"])
    ax.set_ylim(0, 750)
    ax.set_yticks([0, 100, 200, 300, 400, 500, 600, 700, 750])
    ax.set_clip_on(True)
    ax.set_title(f"{label} {title}", fontsize=24, weight="bold")
    ax.grid(True, color="gray", alpha=0.3, linewidth=0.5)
    ax.minorticks_on()

    # Per-day depth-averaged simulated concentration for this case.
    day_means = [(t, df[df["DAY"] == t]["CONC_RATIO_SIMULATED"].mean()) for t in DAYS]
    mean_lines = [f"Day {t} $\\bar{{C}}$ = {m:.2f}" for t, m in day_means]

    # Rate constants + per-day means in a rounded white box.
    box_lines = list(rates) + mean_lines
    n_lines = len(box_lines)
    line_step = 0.063          # vertical spacing between lines (axes coords)
    pad_top = 0.040            # padding from top of box to top of first line
    pad_bot = 0.020            # padding from bottom of last line to box bottom
    box_x, box_y = 0.50, 0.06
    box_w = 0.46
    box_h = pad_top + pad_bot + n_lines * line_step

    ax.add_patch(FancyBboxPatch(
        (box_x, box_y), box_w, box_h,
        transform=ax.transAxes,
        boxstyle="round,pad=0.005,rounding_size=0.03",
        facecolor="white", edgecolor="black", linewidth=1.6,
        clip_on=False, zorder=10,
    ))
    line_top_y = box_y + box_h - pad_top
    for i, line in enumerate(box_lines):
        ax.text(box_x + box_w / 2, line_top_y - i * line_step,
                line, transform=ax.transAxes,
                fontsize=24, weight="normal",
                ha="center", va="top", color="black", zorder=11)


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

    # Force Times New Roman everywhere (titles, ticks, labels, legend,
    # panel labels, RMSE box, math symbols).
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman", "DejaVu Serif"]
    plt.rcParams["mathtext.fontset"] = "stix"
    plt.rcParams["axes.unicode_minus"] = False
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(19.2, 11.9))

    for ax, sheet, ptitle, plabel, prates in zip(
        axes, SHEETS, PANELS, PANEL_LABELS, PANEL_RATES
    ):
        panel(ax, sheets[sheet], ptitle, plabel, prates)

    # Panel-specific axis label / tick handling, matching the original script.
    axes[0].set_ylabel("Height above the column base (cm)", fontsize=24)
    axes[0].tick_params(axis="both", labelsize=22, pad=10)

    axes[1].tick_params(axis="x", labelsize=22, pad=10)
    axes[1].tick_params(axis="y", labelleft=False, direction="in")

    axes[2].tick_params(axis="x", labelsize=22, pad=10)
    axes[2].tick_params(axis="y", direction="in", labelleft=False,
                        labelright=True, labelsize=22, pad=10)
    axes[2].tick_params(right=True, direction="out")

    fig.tight_layout()

    # Single shared legend below all three panels.
    # matplotlib's legend with ncol=N fills column-major, so we interleave
    # the (simulated, analytical) pairs so the rendered layout is:
    #   Row 1 (dashed lines):     Simulated t=1, t=2, t=3
    #   Row 2 (scatter markers):  Analytical t=1, t=2, t=3
    handles, labels = axes[0].get_legend_handles_labels()
    n = len(DAYS)
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
    out_300 = os.path.join(figures_dir, "PHREEQC_Benchmarking_AT_SIMULATED_DEPTHS_300DPI.png")
    out_600 = os.path.join(figures_dir, "PHREEQC_Benchmarking_AT_SIMULATED_DEPTHS_600DPI.png")
    out_pdf = os.path.join(figures_dir, "PHREEQC_Benchmarking_AT_SIMULATED_DEPTHS_Vector.pdf")
    out_svg = os.path.join(figures_dir, "PHREEQC_Benchmarking_AT_SIMULATED_DEPTHS_Vector.svg")
    out_eps = os.path.join(figures_dir, "PHREEQC_Benchmarking_AT_SIMULATED_DEPTHS_Vector.eps")

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
