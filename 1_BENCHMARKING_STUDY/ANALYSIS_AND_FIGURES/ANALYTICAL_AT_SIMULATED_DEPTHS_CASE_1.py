"""
Compute the Ogata-Banks (1961) 1-D analytical advection-dispersion solution
at the SAME depths reported in the simulated CASE_1 sheet of
RESULTS_BENCHMARKING_ANALYTICAL_SOLUTION_750CM.xlsx (column 'Y').

Three new columns are appended (or overwritten) on the CASE_1 sheet:
    CONC_RATIO_ANALYTICAL_AT_Y_DAY_1
    CONC_RATIO_ANALYTICAL_AT_Y_DAY_2
    CONC_RATIO_ANALYTICAL_AT_Y_DAY_3

IMPORTANT: openpyxl strips cached formula values on every save. To avoid
silently nuking values in CASE_2 / CASE_3 (which contain formulas), this
script reads ALL sheets first via pandas (which extracts cached formula
values), then writes ALL sheets back. The net effect is that every formula
in the workbook is converted to its cached numerical value - a one-time,
non-reversible conversion. The original file is in git, so you can restore
it with `git checkout -- <file>` if you need formulas back.

Singularity handling: X_LOCAL = COLUMN_LENGTH - Y is zero at Y = 750 cm
(the inlet boundary). That single depth is shifted to 749.99 cm only for
the analytical evaluation; the stored Y column itself is not modified.

A 3-panel comparison figure (analytical vs simulated, one per day) is shown
and saved to PNG.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import special

# Physical constants (matching ERROR_COMPUTATION_CASE_1_SOLUTE_MOVEMENT.py)
U_DARCY = 25.648                       # Darcy velocity (cm/day)
THETA_SATURATED = 0.2817               # saturated moisture content / porosity
U_PORE = U_DARCY / THETA_SATURATED     # pore-water velocity (cm/day)
DISPERSIVITY = 75.0                    # alpha (cm)
D_DISPERSION = DISPERSIVITY * U_PORE   # dispersion coefficient D = alpha*v (cm^2/day)
C_INJECTED = 1.0                       # injected concentration ratio at boundary
COLUMN_LENGTH = 750.0                  # column length (cm)

XLSX_FILE = "RESULTS_BENCHMARKING_ANALYTICAL_SOLUTION_750CM.xlsx"
SHEET = "CASE_1"
DAYS = [0, 1, 2, 3]
SHIFT_TO = 749.99                      # avoid X_LOCAL = 0 at the inlet
DAY_COLORS = {0: "red", 1: "blue", 2: "green", 3: "orange"}


def ogata_banks(y_values, t_days):
    """Vectorized Ogata-Banks C/C0 at depths y_values for elapsed time t_days.

    y is the spatial coordinate as stored in the workbook (cm), with the
    inlet at Y = COLUMN_LENGTH and the column outlet at Y = 0. The local
    distance from the inlet is X_LOCAL = COLUMN_LENGTH - Y.

    For t_days == 0 the analytical solution is identically zero (initial
    condition) and the formula is degenerate (sqrt(0) divisions), so we
    short-circuit that case.
    """
    y = np.asarray(y_values, dtype=float)
    if t_days == 0:
        return np.zeros_like(y)

    y_eval = np.where(np.isclose(y, COLUMN_LENGTH), SHIFT_TO, y)
    x_local = COLUMN_LENGTH - y_eval

    out = np.full_like(y_eval, np.nan)
    valid = (x_local > 0) & np.isfinite(y_eval)
    xl = x_local[valid]

    epsilon = U_PORE * t_days / xl
    eta = D_DISPERSION / (U_PORE * xl)
    sqrt_ee = np.sqrt(epsilon * eta)
    first = special.erfc((1.0 - epsilon) / (2.0 * sqrt_ee))
    second = np.exp(1.0 / eta) * special.erfc((1.0 + epsilon) / (2.0 * sqrt_ee))
    out[valid] = 0.5 * C_INJECTED * (first + second)
    return out


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    xlsx_path = os.path.join(here, XLSX_FILE)

    print(f"Reading ALL sheets from {XLSX_FILE} ...")
    sheets = pd.read_excel(xlsx_path, sheet_name=None)
    for name, sdf in sheets.items():
        n_day = sdf["DAY"].notna().sum() if "DAY" in sdf.columns else "n/a"
        print(f"  '{name}': shape={sdf.shape}, DAY non-null={n_day}")

    df = sheets[SHEET]

    # Compute analytical at each row's Y for T = 1, 2, 3
    y_arr = df["Y"].to_numpy(dtype=float)
    for t in DAYS:
        col = f"CONC_RATIO_ANALYTICAL_AT_Y_DAY_{t}"
        df[col] = ogata_banks(y_arr, t)
        print(f"  -> column {col}: range "
              f"{df[col].min():.6g} .. {df[col].max():.6g}")
    sheets[SHEET] = df

    print(f"Writing ALL sheets back (formulas across workbook -> values) ...")
    try:
        with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
            for name, sdf in sheets.items():
                sdf.to_excel(writer, sheet_name=name, index=False)
    except PermissionError as exc:
        raise RuntimeError(
            f"Could not save '{xlsx_path}'. Close it in Excel and rerun."
        ) from exc
    print(f"  saved: {xlsx_path}")

    # Figure: replicates the style of
    # 1_PHREEQC_BENCHMARKING_STUDY_1_ANALYTICAL_SOLUTION/3_PHREEQC_2DSOIL_BENCHMARKING_COMPARATIVE_CURVES.py
    # (panel (a) for CASE_1), but the analytical scatter uses the new
    # CONC_RATIO_ANALYTICAL_AT_Y_DAY_k columns evaluated on the dense
    # 437-node simulated Y grid instead of the sparse 50-node grid.
    plt.rcParams["font.family"] = "Times New Roman"
    fig, ax = plt.subplots(figsize=(8, 10.8))

    # Use a single day's worth of rows for the analytical scatter (the
    # analytical value depends only on Y, which repeats across days).
    one_day = df[df["DAY"] == 1].sort_values("Y").reset_index(drop=True)

    # Subsample analytical to ~50 evenly-spaced points so the markers look
    # like discrete dots on top of the dashed simulated line, matching the
    # visual density of Figure_1. The dense analytical column in the Excel
    # is untouched - this subsampling is only for the figure.
    N_VIS = 50
    vis_idx = np.linspace(0, len(one_day) - 1, N_VIS, dtype=int)
    analytical_vis = one_day.iloc[vis_idx]

    # Simulated profiles as dashed colored lines (zorder 1, behind scatter).
    for t in DAYS:
        sub = df[df["DAY"] == t].sort_values("Y")
        ax.plot(sub["CONC_RATIO_SIMULATED"], sub["Y"],
                zorder=1, linestyle="--", color=DAY_COLORS[t],
                label=f"Simulated (t = {t} Day)")

    # Analytical profiles as colored scatter markers with black edges.
    for t in DAYS:
        col = f"CONC_RATIO_ANALYTICAL_AT_Y_DAY_{t}"
        ax.scatter(analytical_vis[col], analytical_vis["Y"],
                   zorder=2, color=DAY_COLORS[t], edgecolor="black", s=20,
                   label=f"Analytical (t = {t} Day)")

    ax.set_xlabel("Concentration (mols/l)", fontsize=20, labelpad=10)
    ax.set_xlim(-0.001, 1.0)
    ax.set_ylabel("Height above the column base (cm)", fontsize=20)
    ax.set_ylim(bottom=0, top=750)
    ax.set_yticks([0, 100, 200, 300, 400, 500, 600, 700, 750])
    ax.set_clip_on(True)
    ax.tick_params(axis="both", labelsize=20, pad=10)
    ax.set_title("(a)", fontsize=24)
    ax.grid(True)
    ax.legend(fontsize=14, borderaxespad=0.02, frameon=True,
              framealpha=1.0, markerscale=1.6)

    fig.tight_layout()
    figures_dir = os.path.join(here, "FIGURES")
    os.makedirs(figures_dir, exist_ok=True)
    out_png = os.path.join(figures_dir, "CASE_1_AT_SIMULATED_DEPTHS_300DPI.png")
    out_pdf = os.path.join(figures_dir, "CASE_1_AT_SIMULATED_DEPTHS_VECTOR.pdf")
    fig.savefig(out_png, dpi=300, bbox_inches="tight",
                facecolor="white", edgecolor="none", format="png")
    fig.savefig(out_pdf, bbox_inches="tight",
                facecolor="white", edgecolor="none", format="pdf")
    print(f"Saved figure: {out_png}")
    print(f"Saved figure: {out_pdf}")
    plt.show()


if __name__ == "__main__":
    main()
