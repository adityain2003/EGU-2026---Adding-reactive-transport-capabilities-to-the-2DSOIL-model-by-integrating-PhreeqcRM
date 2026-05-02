"""
Publication figures for the cation-exchange benchmark: 2DSoil-PhreeqcRM
vs IPhreeqc reference, 5 species, 4 time snapshots (t = 0, 1, 2, 3 days).

Produces two figures, both styled to match the analytical-benchmark figure
(Times New Roman, dashed simulated lines, scatter IPhreeqc markers, bold
(a)/(b)/(c) corner labels, shared legend below, species name as panel
title):

  FIGURES/CATIONS_300DPI.png + .pdf   - 3-panel: Ca2+, Na+, K+
  FIGURES/ANIONS_300DPI.png  + .pdf   - 2-panel: Cl-, NO3-

Per-species RMSE values live in RESULTS_CATION_EXCHANGE_ERROR_METRICS.txt
(and the matching .xlsx) for the manuscript table; they are not drawn on
the figure so the panels read as just the species profile.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

XLSX_FILE = "RESULTS_100cm_1cm_ALL_NODES.xlsx"
FIGURES_DIR = "FIGURES"

DAYS_PLOTTED = [0, 1, 2, 3]
DAY_SECONDS = {0: 0, 1: 86400, 2: 172800, 3: 259200}
# Wong (2011) colorblind-safe palette: black, blue, bluish green, vermillion.
DAY_COLORS = {0: "#000000", 1: "#0072B2", 2: "#009E73", 3: "#D55E00"}
DAY_MARKERS = {0: "o", 1: "s", 2: "^", 3: "D"}

# (panel_label, species_label, species_pretty, species_xlabel, sim_col, ref_col, xlim)
CATIONS = [
    ("(a)", "Ca2+", r"Ca$^{2+}$",   "Concentration (mmol/L)",
     "Ca2+ 2DSoil-PhreeqcRM", "Ca2+ IPhreeqc", (-0.02, 0.6)),
    ("(b)", "Na+",  r"Na$^{+}$",    "Concentration (mmol/L)",
     "Na+ 2DSoil-PhreeqcRM",  "Na+ IPhreeqc",  (-0.005, 1.05)),
    ("(c)", "K+",   r"K$^{+}$",     "Concentration (mmol/L)",
     "K+ 2DSoil-PhreeqcRM",   "K+ IPhreeqc",   (-0.005, 1.20)),
]
ANIONS = [
    ("(a)", "Cl-",  r"Cl$^{-}$",    "Concentration (mmol/L)",
     "Cl- 2DSoil-PhreeqcRM",  "Cl- IPhreeqc",  (-0.005, 1.25)),
    ("(b)", "NO3-", r"NO$_{3}^{-}$", "Concentration (mmol/L)",
     "NO3- 2DSoil-PhreeqcRM", "NO3- IPhreeqc", (-0.005, 1.25)),
]

N_VIS = 50    # subsample for the analytical scatter, like the benchmarking figure


def slice_day(df, t_sec, sim_col, ref_col):
    """Sorted (sim_y, sim_v, ref_y, ref_v) for one day."""
    sim_df = (
        df[df["Time ABS 2DSoil-PhreeqcRM"] == t_sec]
        [["Y_ABS 2DSoil_PhreeqcRM", sim_col]].dropna()
        .sort_values("Y_ABS 2DSoil_PhreeqcRM").reset_index(drop=True)
    )
    ref_df = (
        df[df["time Iphreeqc"] == t_sec]
        [["Y Iphreeqc", ref_col]].dropna()
        .sort_values("Y Iphreeqc").reset_index(drop=True)
    )
    return (
        sim_df["Y_ABS 2DSoil_PhreeqcRM"].to_numpy(),
        sim_df[sim_col].to_numpy(),
        ref_df["Y Iphreeqc"].to_numpy(),
        ref_df[ref_col].to_numpy(),
    )


def draw_panel(ax, df, label, species_pretty, xlabel, sim_col, ref_col, xlim):
    # Simulated profiles as dashed colored lines (one per day).
    for d in DAYS_PLOTTED:
        sim_y, sim_v, ref_y, ref_v = slice_day(df, DAY_SECONDS[d], sim_col, ref_col)
        if sim_v.size:
            ax.plot(sim_v, sim_y,
                    zorder=1, linestyle="--", color=DAY_COLORS[d],
                    label=f"Simulated (Day {d})")

    # IPhreeqc as colored scatter markers, subsampled for clarity.
    for d in DAYS_PLOTTED:
        sim_y, sim_v, ref_y, ref_v = slice_day(df, DAY_SECONDS[d], sim_col, ref_col)
        if ref_v.size == 0:
            continue
        n = min(N_VIS, ref_v.size)
        idx = np.linspace(0, ref_v.size - 1, n, dtype=int)
        ax.scatter(ref_v[idx], ref_y[idx],
                   zorder=2, color=DAY_COLORS[d], edgecolor="black", s=20,
                   marker=DAY_MARKERS[d],
                   label=f"IPhreeqc (Day {d})")

    ax.set_xlabel(xlabel, fontsize=24, labelpad=10)
    ax.set_xlim(*xlim)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.grid(True, color="gray", alpha=0.3, linewidth=0.5)
    ax.minorticks_on()
    ax.set_clip_on(True)
    ax.set_title(f"{label} {species_pretty}", fontsize=24, weight="bold")


def add_shared_legend_below(fig, ref_ax, n_days):
    """Two-row shared legend below all panels: simulated row, then IPhreeqc row."""
    handles, labels = ref_ax.get_legend_handles_labels()
    # Reorder for column-major fill so row 1 = simulated, row 2 = IPhreeqc.
    interleaved_h, interleaved_l = [], []
    for i in range(n_days):
        interleaved_h.extend([handles[i], handles[i + n_days]])
        interleaved_l.extend([labels[i], labels[i + n_days]])
    fig.subplots_adjust(bottom=0.26)
    fig.legend(interleaved_h, interleaved_l, loc="lower center", ncol=n_days,
               fontsize=24, frameon=True, framealpha=1.0, markerscale=1.6,
               bbox_to_anchor=(0.5, 0.01))


def style_axis(ax, position):
    """Position-specific tick handling matching the benchmarking layout."""
    if position == "left":
        ax.set_ylabel("Height above the column base (cm)", fontsize=24)
        ax.tick_params(axis="both", labelsize=22, pad=10)
    elif position == "middle":
        ax.tick_params(axis="x", labelsize=22, pad=10)
        ax.tick_params(axis="y", labelleft=False, direction="in")
    elif position == "right":
        ax.tick_params(axis="x", labelsize=22, pad=10)
        ax.tick_params(axis="y", direction="in", labelleft=False,
                       labelright=True, labelsize=22, pad=10)
        ax.tick_params(right=True, direction="out")
    elif position == "right_only":   # 2-panel layout: right panel only
        ax.tick_params(axis="x", labelsize=22, pad=10)
        ax.tick_params(axis="y", direction="in", labelleft=False,
                       labelright=True, labelsize=22, pad=10)
        ax.tick_params(right=True, direction="out")


def make_figure(df, panels, layout, out_basename, here):
    n = len(panels)
    if layout == "3":
        fig, axes = plt.subplots(1, 3, figsize=(19.2, 11.9))
        positions = ["left", "middle", "right"]
    elif layout == "2":
        fig, axes = plt.subplots(1, 2, figsize=(13.0, 11.9))
        positions = ["left", "right_only"]
    else:
        raise ValueError(layout)

    for ax, (label, _, species_pretty, xlabel, sim_col, ref_col, xlim), pos in zip(
        axes, panels, positions
    ):
        draw_panel(ax, df, label, species_pretty, xlabel, sim_col, ref_col, xlim)
        style_axis(ax, pos)

    fig.tight_layout()
    add_shared_legend_below(fig, axes[0], len(DAYS_PLOTTED))

    figures_dir = os.path.join(here, FIGURES_DIR)
    os.makedirs(figures_dir, exist_ok=True)
    out_png_300 = os.path.join(figures_dir, f"{out_basename}_300DPI.png")
    out_png_600 = os.path.join(figures_dir, f"{out_basename}_600DPI.png")
    out_pdf = os.path.join(figures_dir, f"{out_basename}_VECTOR.pdf")
    fig.savefig(out_png_300, dpi=300, bbox_inches="tight",
                facecolor="white", edgecolor="none", format="png")
    fig.savefig(out_png_600, dpi=600, bbox_inches="tight",
                facecolor="white", edgecolor="none", format="png")
    fig.savefig(out_pdf, bbox_inches="tight",
                facecolor="white", edgecolor="none", format="pdf")
    print(f"Saved: {out_png_300}")
    print(f"Saved: {out_png_600}")
    print(f"Saved: {out_pdf}")
    return fig


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    xlsx_path = os.path.join(here, XLSX_FILE)
    df = pd.read_excel(xlsx_path)
    print(f"Loaded {XLSX_FILE}: shape={df.shape}")

    # Fix Times New Roman for everything (titles, ticks, labels, legend, mathtext).
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman", "DejaVu Serif"]
    plt.rcParams["mathtext.fontset"] = "stix"
    plt.rcParams["axes.unicode_minus"] = False

    make_figure(df, CATIONS, "3", "CATIONS", here)
    make_figure(df, ANIONS,  "2", "ANIONS",  here)

    plt.show()


if __name__ == "__main__":
    main()
