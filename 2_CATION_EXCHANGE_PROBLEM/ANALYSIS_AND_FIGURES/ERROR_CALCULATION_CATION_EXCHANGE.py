"""
Error metrics for the cation-exchange benchmark: 2DSoil-PhreeqcRM vs
IPhreeqc reference for 5 species (Ca2+, Cl-, Na+, K+, NO3-) over days
1-3, on a 100 cm column at 1 cm node spacing.

The two depth grids do not align:
  - Simulated: Y_ABS 2DSoil_PhreeqcRM, 0.0..100.0 cm (node-centered)
  - Reference: Y Iphreeqc,             0.5..99.5 cm (cell-centered, offset 0.5 cm)

The IPhreeqc reference is linearly interpolated onto the simulated Y grid
before metrics are computed, so subtraction is point-wise without an
off-by-half-cell error.

A per-(species, day) mask of (sim > 0.01) & (ref > 0.01) excludes near-zero
values that would inflate MAPE; this matches the original analysis policy.

Outputs in this folder:
  RESULTS_CATION_EXCHANGE_ERROR_METRICS.txt   plain-text report
  RESULTS_CATION_EXCHANGE_ERROR_METRICS.xlsx  multi-sheet workbook
"""

import os
import numpy as np
import pandas as pd

XLSX_FILE = "RESULTS_100cm_1cm_ALL_NODES.xlsx"
OUT_TXT = "RESULTS_CATION_EXCHANGE_ERROR_METRICS.txt"
OUT_XLSX = "RESULTS_CATION_EXCHANGE_ERROR_METRICS.xlsx"

# day index -> seconds from t=0
DAYS_SECONDS = {1: 86400, 2: 172800, 3: 259200}

# (label, simulated column, reference column)
SPECIES = [
    ("Ca2+", "Ca2+ 2DSoil-PhreeqcRM", "Ca2+ IPhreeqc"),
    ("Cl-",  "Cl- 2DSoil-PhreeqcRM",  "Cl- IPhreeqc"),
    ("Na+",  "Na+ 2DSoil-PhreeqcRM",  "Na+ IPhreeqc"),
    ("K+",   "K+ 2DSoil-PhreeqcRM",   "K+ IPhreeqc"),
    ("NO3-", "NO3- 2DSoil-PhreeqcRM", "NO3- IPhreeqc"),
]

MASK_THRESHOLD = 0.01  # mmol/L; values at or below this on either side are dropped


def compute_metrics(sim, ref):
    """Return RMSE/MAE/MaxAE/MBE/NRMSE_%/R2/NSE/MAPE_%/SMAPE_% for a paired vector."""
    sim = np.asarray(sim, dtype=float)
    ref = np.asarray(ref, dtype=float)
    n = sim.size
    if n == 0:
        nan = float("nan")
        return {"N": 0, "RMSE": nan, "MAE": nan, "MaxAbsError": nan,
                "MBE": nan, "NRMSE_%": nan, "R2": nan, "NSE": nan,
                "MAPE_%": nan, "SMAPE_%": nan}
    err = sim - ref
    rmse = float(np.sqrt(np.mean(err ** 2)))
    mae = float(np.mean(np.abs(err)))
    max_ae = float(np.max(np.abs(err)))
    mbe = float(np.mean(err))
    ref_range = float(ref.max() - ref.min())
    nrmse_pct = (rmse / ref_range * 100.0) if ref_range > 0 else float("nan")
    if np.var(ref) > 0:
        nse = 1.0 - float(np.sum(err ** 2)) / float(np.sum((ref - ref.mean()) ** 2))
        if np.std(sim) > 0:
            r = float(np.corrcoef(sim, ref)[0, 1])
            r2 = r * r
        else:
            r2 = float("nan")
    else:
        nse = float("nan")
        r2 = float("nan")
    # MAPE only well-defined when ref is non-zero (mask already ensures > 0).
    mape_pct = float(np.mean(np.abs(err / ref))) * 100.0
    smape_pct = float(np.mean(2.0 * np.abs(err) / (np.abs(sim) + np.abs(ref)))) * 100.0
    return {"N": n, "RMSE": rmse, "MAE": mae, "MaxAbsError": max_ae,
            "MBE": mbe, "NRMSE_%": nrmse_pct, "R2": r2, "NSE": nse,
            "MAPE_%": mape_pct, "SMAPE_%": smape_pct}


def evaluate_species(df, label, sim_col, ref_col):
    """Per-day metrics + the paired (after interp + mask) frame for one species."""
    rows = []
    paired_frames = []
    for day, t_sec in DAYS_SECONDS.items():
        sim_df = (
            df[df["Time ABS 2DSoil-PhreeqcRM"] == t_sec]
            [["Y_ABS 2DSoil_PhreeqcRM", sim_col]]
            .dropna()
            .sort_values("Y_ABS 2DSoil_PhreeqcRM")
            .reset_index(drop=True)
        )
        ref_df = (
            df[df["time Iphreeqc"] == t_sec]
            [["Y Iphreeqc", ref_col]]
            .dropna()
            .sort_values("Y Iphreeqc")
            .reset_index(drop=True)
        )
        if sim_df.empty or ref_df.empty:
            continue

        sim_y = sim_df["Y_ABS 2DSoil_PhreeqcRM"].to_numpy()
        sim_v = sim_df[sim_col].to_numpy()
        ref_y = ref_df["Y Iphreeqc"].to_numpy()
        ref_v = ref_df[ref_col].to_numpy()

        # Linearly interpolate the reference onto the simulated Y grid.
        ref_v_at_sim = np.interp(sim_y, ref_y, ref_v)

        # Drop near-zero pairs (matches the original analysis policy).
        mask = (sim_v > MASK_THRESHOLD) & (ref_v_at_sim > MASK_THRESHOLD)
        if mask.sum() < 5:
            continue

        sim_m = sim_v[mask]
        ref_m = ref_v_at_sim[mask]
        m = compute_metrics(sim_m, ref_m)
        rows.append({"Species": label, "DAY": day, **m})

        paired_frames.append(pd.DataFrame({
            "Species": label, "DAY": day,
            "Y": sim_y[mask],
            "REF_INTERP": ref_m,
            "SIM": sim_m,
            "ABS_ERROR": np.abs(sim_m - ref_m),
        }))

    summary = pd.DataFrame(rows)
    paired = pd.concat(paired_frames, ignore_index=True) if paired_frames else pd.DataFrame()
    return summary, paired


def build_report(summary_all, agg, overall, worst_points):
    bar = "=" * 96
    return "\n".join([
        bar,
        "Error metrics: 2DSoil-PhreeqcRM vs IPhreeqc reference  (cation-exchange benchmark)",
        "Domain: 100 cm column, 1 cm node spacing.",
        "Days compared: 1, 2, 3 (DAY 0 = initial condition; DAY 4-5 dropped because the",
        "anions have left the column and the cations are too dilute to compare meaningfully).",
        "Mask: pairs with sim <= 0.01 OR ref <= 0.01 mmol/L are excluded (avoid MAPE blow-up).",
        "IPhreeqc reference linearly interpolated from cell-centered Y (0.5..99.5 cm) onto",
        "the simulated node grid (0..100 cm) before computing metrics.",
        bar,
        "",
        "Per-species, per-day metrics:",
        summary_all.to_string(index=False),
        "",
        "Aggregate metrics per species (across DAY 1, 2, 3):",
        agg.to_string(),
        "",
        "Overall metrics across ALL species and ALL days:",
        overall.to_string(),
        "",
        "Worst pointwise mismatch per species:",
        worst_points.to_string(index=False),
        "",
        "Metric definitions:",
        "  N            number of paired (interpolated, masked) depths used",
        "  RMSE         root mean squared error (sim - ref)              [mmol/L]",
        "  MAE          mean absolute error                              [mmol/L]",
        "  MaxAbsError  largest |error| seen                             [mmol/L]",
        "  MBE          mean bias error  (positive = sim overshoots)     [mmol/L]",
        "  NRMSE_%      RMSE normalised by ref range, as percent",
        "  R2           Pearson coefficient of determination",
        "  NSE          Nash-Sutcliffe efficiency (1.0 = perfect match)",
        "  MAPE_%       mean absolute percentage error                   [%]",
        "  SMAPE_%      symmetric MAPE                                   [%]",
        "  Pooled_RMSE  sqrt( sum(N_i RMSE_i^2) / sum(N_i) ), N-weighted",
        "  Simple_RMSE  RMSE on the concatenated residual vector for the species",
        bar,
    ])


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    xlsx_path = os.path.join(here, XLSX_FILE)

    print(f"Reading {XLSX_FILE} ...")
    df = pd.read_excel(xlsx_path)
    print(f"  shape: {df.shape}")

    summary_frames = []
    paired_frames = []
    for label, sim_col, ref_col in SPECIES:
        s, p = evaluate_species(df, label, sim_col, ref_col)
        summary_frames.append(s)
        paired_frames.append(p)
    summary_all = pd.concat(summary_frames, ignore_index=True)
    paired_all = pd.concat(paired_frames, ignore_index=True)

    pd.set_option("display.float_format", lambda v: f"{v:.6g}")

    # Per-species aggregates
    agg = summary_all.groupby("Species").apply(
        lambda g: pd.Series({
            "Mean_RMSE": g["RMSE"].mean(),
            "Pooled_RMSE": np.sqrt((g["RMSE"] ** 2 * g["N"]).sum() / g["N"].sum()),
            "Mean_MAE": g["MAE"].mean(),
            "Max_AbsError": g["MaxAbsError"].max(),
            "Max_AbsError_DAY": int(g.loc[g["MaxAbsError"].idxmax(), "DAY"]),
            "Mean_R2": g["R2"].mean(skipna=True),
            "Mean_NSE": g["NSE"].mean(skipna=True),
        }),
        include_groups=False,
    )
    simple_rmse_per_species = (
        paired_all.groupby("Species")["ABS_ERROR"]
        .apply(lambda x: float(np.sqrt(np.mean(x.values ** 2))))
    )
    agg.insert(2, "Simple_RMSE", simple_rmse_per_species)

    # Overall
    simple_rmse_overall = float(np.sqrt(np.mean(paired_all["ABS_ERROR"].values ** 2)))
    overall = pd.Series({
        "Mean_RMSE": summary_all["RMSE"].mean(),
        "Pooled_RMSE": float(np.sqrt(
            (summary_all["RMSE"] ** 2 * summary_all["N"]).sum() / summary_all["N"].sum()
        )),
        "Simple_RMSE": simple_rmse_overall,
        "Mean_MAE": summary_all["MAE"].mean(),
        "Max_AbsError": summary_all["MaxAbsError"].max(),
        "Mean_R2": summary_all["R2"].mean(skipna=True),
        "Mean_NSE": summary_all["NSE"].mean(skipna=True),
    }, name="ALL_SPECIES_ALL_DAYS")

    worst_idx = paired_all.groupby("Species")["ABS_ERROR"].idxmax()
    worst_points = paired_all.loc[
        worst_idx, ["Species", "DAY", "Y", "REF_INTERP", "SIM", "ABS_ERROR"]
    ].reset_index(drop=True)

    report = build_report(summary_all, agg, overall, worst_points)
    print(report)

    txt_path = os.path.join(here, OUT_TXT)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(report + "\n")

    out_path = os.path.join(here, OUT_XLSX)
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        summary_all.to_excel(writer, sheet_name="METRICS_SUMMARY", index=False)
        agg.to_excel(writer, sheet_name="METRICS_AGGREGATE")
        overall.to_frame().T.to_excel(writer, sheet_name="METRICS_OVERALL", index=False)
        worst_points.to_excel(writer, sheet_name="WORST_POINT_PER_SPECIES", index=False)
        paired_all.to_excel(writer, sheet_name="PAIRED_POINTWISE", index=False)

    print(f"\nWrote text report to: {txt_path}")
    print(f"Wrote Excel results to: {out_path}")


if __name__ == "__main__":
    main()
