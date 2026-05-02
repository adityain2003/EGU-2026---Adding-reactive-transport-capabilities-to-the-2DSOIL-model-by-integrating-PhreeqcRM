"""
Compute the van Genuchten (1981) 1-D analytical solution for advection-
dispersion with first-order decay AND zero-order production at the SAME
depths reported in the simulated CASE_3 sheet of
RESULTS_BENCHMARKING_ANALYTICAL_SOLUTION_750CM.xlsx (column 'Y').

Mirrors the CASE_2 script but uses the full van Genuchten form because
gamma > 0 here. The full solution is:

    C/C0 = (1 - gamma/mu) * H_TERM + M_TERM

H_TERM (same as CASE_2):

    H_TERM = 0.5 * exp((v - U)*x / (2D)) * erfc((x - U*t) / (2*sqrt(D*t)))
           + 0.5 * exp((v + U)*x / (2D)) * erfc((x + U*t) / (2*sqrt(D*t)))
    U      = v * sqrt(1 + 4*mu*D / v^2)

M_TERM (zero-order production tail):

    M_TERM = (gamma/mu) * exp(-mu*t) * [
                0.5 * erfc((x - v*t) / (2*sqrt(D*t)))
              + 0.5 * exp(v*x/D) * erfc((x + v*t) / (2*sqrt(D*t)))
             ]
           + (gamma/mu) * (1 - exp(-mu*t))

CASE_3 uses gamma = 1.0e-6 * 86400 day^-1, so gamma/mu = 1/3.

Adds CONC_RATIO_ANALYTICAL_AT_Y_DAY_0/1/2/3 columns to CASE_3 sheet, and
generates a Figure_1-style "(c)" panel.

Same workbook caveat as CASE_1/CASE_2 scripts: read all sheets first, write
all sheets back. The workbook was already converted to all-values during
the CASE_1 run on 2026-05-01, so other sheets are unchanged.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import special

# Physical constants (matching ERROR_COMPUTATION_CASE_3_SOLUTE_BIODEGRADATION.py)
U_DARCY = 25.648                       # Darcy velocity (cm/day)
THETA_SATURATED = 0.2817               # saturated moisture content / porosity
U_PORE = U_DARCY / THETA_SATURATED     # pore-water velocity (cm/day)
DISPERSIVITY = 75.0                    # alpha (cm)
D_DISPERSION = DISPERSIVITY * U_PORE   # dispersion coefficient (cm^2/day)
C_INJECTED = 1.0                       # injected concentration ratio at boundary
COLUMN_LENGTH = 750.0                  # column length (cm)
MU = 3.0e-6 * 86400.0                  # first-order decay rate (1/day) = 0.2592
GAMMA = 1.0e-6 * 86400.0               # zero-order production (1/day) = 0.0864

XLSX_FILE = "RESULTS_BENCHMARKING_ANALYTICAL_SOLUTION_750CM.xlsx"
SHEET = "CASE_3"
DAYS = [0, 1, 2, 3]
DAY_COLORS = {0: "red", 1: "blue", 2: "green", 3: "orange"}


def van_genuchten_full(y_values, t_days):
    """Vectorized van Genuchten 1981 C/C0 with first-order decay AND
    zero-order production.

    y is the spatial coordinate as stored in the workbook (cm), with the
    inlet at Y = COLUMN_LENGTH and the column outlet at Y = 0. The local
    distance from the inlet is X_LOCAL = COLUMN_LENGTH - Y.

    For t_days == 0 the analytical solution is the zero initial condition
    (and the formula is degenerate via sqrt(D*0) = 0), so we short-circuit.
    X_LOCAL = 0 (Y = 750) is well-defined: H_TERM = 1 and M_TERM = gamma/mu,
    so C/C0 = (1 - g/m)*1 + g/m = 1 at the inlet for any t > 0.
    """
    y = np.asarray(y_values, dtype=float)
    if t_days == 0:
        return np.zeros_like(y)

    x_local = COLUMN_LENGTH - y
    out = np.full_like(y, np.nan)
    valid = (x_local >= 0) & np.isfinite(y)
    xl = x_local[valid]

    u_term = U_PORE * np.sqrt(1.0 + 4.0 * MU * D_DISPERSION / (U_PORE ** 2))
    sqrt_dt = np.sqrt(D_DISPERSION * t_days)
    gamma_by_mu = GAMMA / MU
    decay_factor = np.exp(-MU * t_days)

    # H_TERM
    arg_minus = (xl - u_term * t_days) / (2.0 * sqrt_dt)
    arg_plus = (xl + u_term * t_days) / (2.0 * sqrt_dt)
    exp_minus = np.exp((U_PORE - u_term) * xl / (2.0 * D_DISPERSION))
    exp_plus = np.exp((U_PORE + u_term) * xl / (2.0 * D_DISPERSION))
    h_term = (
        0.5 * exp_minus * special.erfc(arg_minus)
        + 0.5 * exp_plus * special.erfc(arg_plus)
    )

    # M_TERM (zero-order production)
    m_arg_minus = (xl - U_PORE * t_days) / (2.0 * sqrt_dt)
    m_arg_plus = (xl + U_PORE * t_days) / (2.0 * sqrt_dt)
    m_exp = np.exp(U_PORE * xl / D_DISPERSION)
    m_inner = (
        0.5 * special.erfc(m_arg_minus)
        + 0.5 * m_exp * special.erfc(m_arg_plus)
    )
    m_term = gamma_by_mu * decay_factor * m_inner + gamma_by_mu * (1.0 - decay_factor)

    c = (1.0 - gamma_by_mu) * h_term + m_term
    out[valid] = C_INJECTED * c
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
    y_arr = df["Y"].to_numpy(dtype=float)

    u_term = U_PORE * np.sqrt(1.0 + 4.0 * MU * D_DISPERSION / (U_PORE ** 2))
    print(f"\nU_PORE = {U_PORE:.4f} cm/day, D = {D_DISPERSION:.2f} cm^2/day, "
          f"MU = {MU:.4f} 1/day, GAMMA = {GAMMA:.4f} 1/day, "
          f"GAMMA/MU = {GAMMA/MU:.4f}, U_term = {u_term:.4f} cm/day")

    for t in DAYS:
        col = f"CONC_RATIO_ANALYTICAL_AT_Y_DAY_{t}"
        df[col] = van_genuchten_full(y_arr, t)
        print(f"  -> column {col}: range "
              f"{df[col].min():.6g} .. {df[col].max():.6g}")
    sheets[SHEET] = df

    print(f"\nWriting ALL sheets back ...")
    try:
        with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
            for name, sdf in sheets.items():
                sdf.to_excel(writer, sheet_name=name, index=False)
    except PermissionError as exc:
        raise RuntimeError(
            f"Could not save '{xlsx_path}'. Close it in Excel and rerun."
        ) from exc
    print(f"  saved: {xlsx_path}")

    # On-grid error report
    print("\nOn-grid error (CASE_3, no interpolation):")
    for t in [1, 2, 3]:
        sub = df[df["DAY"] == t].sort_values("Y")
        sim = sub["CONC_RATIO_SIMULATED"].dropna().to_numpy()
        ana = sub.loc[sub["CONC_RATIO_SIMULATED"].notna(),
                      f"CONC_RATIO_ANALYTICAL_AT_Y_DAY_{t}"].to_numpy()
        err = sim - ana
        rmse = float(np.sqrt(np.mean(err ** 2)))
        mae = float(np.mean(np.abs(err)))
        maxae = float(np.max(np.abs(err)))
        print(f"  DAY {t}: N={len(sim):4d}  RMSE={rmse:.6e}  "
              f"MAE={mae:.6e}  MaxAE={maxae:.6e}")

    # Figure: Figure_1-style panel (c)
    plt.rcParams["font.family"] = "Times New Roman"
    fig, ax = plt.subplots(figsize=(8, 10.8))

    one_day = df[df["DAY"] == 1].sort_values("Y").reset_index(drop=True)
    N_VIS = 50
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
    ax.set_ylabel("Height above the column base (cm)", fontsize=20)
    ax.set_ylim(bottom=0, top=750)
    ax.set_yticks([0, 100, 200, 300, 400, 500, 600, 700, 750])
    ax.set_clip_on(True)
    ax.tick_params(axis="both", labelsize=20, pad=10)
    ax.set_title("(c)", fontsize=24)
    ax.grid(True)
    ax.legend(fontsize=14, borderaxespad=0.02, frameon=True,
              framealpha=1.0, markerscale=1.6)

    fig.tight_layout()
    figures_dir = os.path.join(here, "FIGURES")
    os.makedirs(figures_dir, exist_ok=True)
    out_png = os.path.join(figures_dir, "CASE_3_AT_SIMULATED_DEPTHS_300DPI.png")
    out_pdf = os.path.join(figures_dir, "CASE_3_AT_SIMULATED_DEPTHS_VECTOR.pdf")
    fig.savefig(out_png, dpi=300, bbox_inches="tight",
                facecolor="white", edgecolor="none", format="png")
    fig.savefig(out_pdf, bbox_inches="tight",
                facecolor="white", edgecolor="none", format="pdf")
    print(f"\nSaved figure: {out_png}")
    print(f"Saved figure: {out_pdf}")
    plt.show()


if __name__ == "__main__":
    main()
