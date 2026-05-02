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
DAY_COLORS = {1: "blue", 2: "green", 3: "orange"}
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
                label=f"Simulated (t = {t} Day)")

    for t in DAYS:
        col = f"CONC_RATIO_ANALYTICAL_AT_Y_DAY_{t}"
        ax.scatter(analytical_vis[col], analytical_vis["Y"],
                   zorder=2, color=DAY_COLORS[t], edgecolor="black", s=20,
                   label=f"Analytical (t = {t} Day)")

    ax.set_xlabel("Concentration (mols/l)", fontsize=20, labelpad=10)
    ax.set_xlim(-0.001, 1.0)
    ax.set_ylim(0, 750)
    ax.set_yticks([0, 100, 200, 300, 400, 500, 600, 700, 750])
    ax.set_clip_on(True)
    ax.set_title(title, fontsize=18)
    ax.grid(True, color="gray", alpha=0.3, linewidth=0.5)

    # Bold panel letter in upper-left corner inside the plot.
    ax.text(0.03, 0.97, label, transform=ax.transAxes,
            fontsize=22, weight="bold", va="top", ha="left", zorder=12)

    # Pooled RMSE for this case (concatenate residuals across all days,
    # then sqrt(mean(err^2))). Displayed in a rounded white box together
    # with the rate constants for this case.
    all_sim, all_ana = [], []
    for t in DAYS:
        sub = df[df["DAY"] == t].sort_values("Y")
        all_sim.append(sub["CONC_RATIO_SIMULATED"].to_numpy())
        all_ana.append(sub[f"CONC_RATIO_ANALYTICAL_AT_Y_DAY_{t}"].to_numpy())
    all_sim = np.concatenate(all_sim)
    all_ana = np.concatenate(all_ana)
    rmse_overall = float(np.sqrt(np.mean((all_sim - all_ana) ** 2)))

    # Box dimensions: tight padding so the content fills the box evenly.
    n_lines = 1 + len(rates)
    line_step = 0.058          # vertical spacing between lines (axes coords)
    pad_top = 0.040            # padding from top of box to top of first line
    pad_bot = 0.020            # padding from bottom of last line to box bottom
    box_x, box_y = 0.62, 0.06
    box_w = 0.34
    box_h = pad_top + pad_bot + n_lines * line_step

    ax.add_patch(FancyBboxPatch(
        (box_x, box_y), box_w, box_h,
        transform=ax.transAxes,
        boxstyle="round,pad=0.005,rounding_size=0.03",
        facecolor="white", edgecolor="black", linewidth=1.6,
        clip_on=False, zorder=10,
    ))
    # Rates above, RMSE at the bottom. All same font size; only RMSE in bold.
    line_top_y = box_y + box_h - pad_top
    for i, rate in enumerate(rates):
        ax.text(box_x + box_w / 2, line_top_y - i * line_step,
                rate, transform=ax.transAxes,
                fontsize=16, weight="normal",
                ha="center", va="top", color="black", zorder=11)
    ax.text(box_x + box_w / 2, line_top_y - len(rates) * line_step,
            f"RMSE = {rmse_overall:.2e}",
            transform=ax.transAxes, fontsize=16, weight="bold",
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
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(19.2, 10.8))

    for ax, sheet, ptitle, plabel, prates in zip(
        axes, SHEETS, PANELS, PANEL_LABELS, PANEL_RATES
    ):
        panel(ax, sheets[sheet], ptitle, plabel, prates)

    # Panel-specific axis label / tick handling, matching the original script.
    axes[0].set_ylabel("Height above the column base (cm)", fontsize=20)
    axes[0].tick_params(axis="both", labelsize=20, pad=10)

    axes[1].tick_params(axis="x", labelsize=20, pad=10)
    axes[1].tick_params(axis="y", labelleft=False, direction="in")

    axes[2].tick_params(axis="x", labelsize=20, pad=10)
    axes[2].tick_params(axis="y", direction="in", labelleft=False,
                        labelright=True, labelsize=20, pad=10)
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
    fig.subplots_adjust(bottom=0.20)
    fig.legend(interleaved_h, interleaved_l, loc="lower center", ncol=n,
               fontsize=16, frameon=True, framealpha=1.0, markerscale=2.0,
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
