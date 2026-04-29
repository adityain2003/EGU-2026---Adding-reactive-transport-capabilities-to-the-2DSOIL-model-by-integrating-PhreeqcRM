"""
Compute error metrics (RMSE, MAE, MaxAE, MBE, NRMSE, R^2, NSE) comparing
PHREEQC-2DSOIL numerical results against the 1-D analytical solution stored
in RESULTS_BENCHMARKING_ANALYTICAL_SOLUTION_750CM.xlsx.

File layout (per sheet CASE_1 / CASE_2 / CASE_3):
    Simulated columns : Y (cm), CONC_RATIO_SIMULATED, with DAY in {0..5}.
    Analytical columns: Y_ANALYTICAL_DAY_k, CONC_RATIO_ANALYTICAL_DAY_k for
                       k in {0,1,2,3}; only the first 50 rows of the sheet
                       carry analytical values, the rest are NaN.

The simulated Y grid is denser (437 nodes) than the analytical grid
(50 depths), so the simulated profile is linearly interpolated onto the
analytical depths before metrics are computed.
"""

import os
import numpy as np
import pandas as pd

INPUT_FILE = "RESULTS_BENCHMARKING_ANALYTICAL_SOLUTION_750CM.xlsx"
OUTPUT_FILE = "RESULTS_BENCHMARKING_ERROR_METRICS.xlsx"
TXT_OUTPUT_FILE = "RESULTS_BENCHMARKING_ERROR_METRICS.txt"
CASES = ["CASE_1", "CASE_2", "CASE_3"]
ANALYTICAL_DAYS = [1, 2, 3]


def compute_metrics(sim, ana):
    """Return a dict of error metrics comparing sim against ana (1-D arrays)."""
    sim = np.asarray(sim, dtype=float)
    ana = np.asarray(ana, dtype=float)
    err = sim - ana
    n = err.size

    rmse = float(np.sqrt(np.mean(err ** 2)))
    mae = float(np.mean(np.abs(err)))
    max_ae = float(np.max(np.abs(err)))
    mbe = float(np.mean(err))

    ana_range = float(ana.max() - ana.min())
    nrmse_pct = (rmse / ana_range * 100.0) if ana_range > 0 else np.nan

    ana_var = float(np.var(ana))
    if ana_var > 0:
        nse = 1.0 - float(np.sum(err ** 2)) / float(np.sum((ana - ana.mean()) ** 2))
        if np.std(sim) > 0:
            r = float(np.corrcoef(sim, ana)[0, 1])
            r2 = r * r
        else:
            r2 = np.nan
    else:
        nse = np.nan
        r2 = np.nan

    return {
        "N": n,
        "RMSE": rmse,
        "MAE": mae,
        "MaxAbsError": max_ae,
        "MBE": mbe,
        "NRMSE_%": nrmse_pct,
        "R2": r2,
        "NSE": nse,
    }


def load_case(xlsx_path, sheet):
    """Return (sim_by_day, ana_by_day) dicts keyed by DAY index."""
    df = pd.read_excel(xlsx_path, sheet_name=sheet)

    sim_by_day = {}
    for day, sub in df.groupby("DAY"):
        sub = sub[["Y", "CONC_RATIO_SIMULATED"]].dropna()
        sub = sub.sort_values("Y").reset_index(drop=True)
        sim_by_day[int(day)] = sub

    ana_by_day = {}
    for k in ANALYTICAL_DAYS:
        y_col = f"Y_ANALYTICAL_DAY_{k}"
        c_col = f"CONC_RATIO_ANALYTICAL_DAY_{k}"
        sub = df[[y_col, c_col]].dropna()
        sub = sub.rename(columns={y_col: "Y", c_col: "CONC_RATIO_ANALYTICAL"})
        sub = sub.sort_values("Y").reset_index(drop=True)
        ana_by_day[k] = sub

    return sim_by_day, ana_by_day


def evaluate_case(xlsx_path, sheet):
    sim_by_day, ana_by_day = load_case(xlsx_path, sheet)

    rows = []
    paired_frames = []

    for day in ANALYTICAL_DAYS:
        if day not in sim_by_day:
            continue
        sim = sim_by_day[day]
        ana = ana_by_day[day]

        # Interpolate simulated profile onto analytical depths.
        sim_at_ana = np.interp(
            ana["Y"].values,
            sim["Y"].values,
            sim["CONC_RATIO_SIMULATED"].values,
        )

        metrics = compute_metrics(sim_at_ana, ana["CONC_RATIO_ANALYTICAL"].values)
        metrics = {"CASE": sheet, "DAY": day, **metrics}
        rows.append(metrics)

        paired = pd.DataFrame({
            "CASE": sheet,
            "DAY": day,
            "Y": ana["Y"].values,
            "CONC_RATIO_ANALYTICAL": ana["CONC_RATIO_ANALYTICAL"].values,
            "CONC_RATIO_SIMULATED_INTERP": sim_at_ana,
            "ABS_ERROR": np.abs(sim_at_ana - ana["CONC_RATIO_ANALYTICAL"].values),
        })
        paired_frames.append(paired)

    return pd.DataFrame(rows), pd.concat(paired_frames, ignore_index=True)


def build_report(summary_all, agg, worst_points, overall):
    """Return a formatted plain-text report of the error metrics."""
    bar = "=" * 88
    lines = [
        bar,
        "Error metrics: PHREEQC-2DSOIL numerical vs. 1-D analytical solution",
        "Domain depth = 750 cm; metrics in concentration-ratio units (dimensionless)",
        "Days compared: 1, 2, 3 (DAY 0 omitted - identical zero initial condition)",
        "Simulated profile interpolated onto the 50 analytical depths per day.",
        bar,
        "",
        "Per-case, per-day metrics:",
        summary_all.to_string(index=False),
        "",
        "Aggregate metrics per case (across DAY 1, 2, 3):",
        agg.to_string(),
        "",
        "Overall metrics across ALL cases and ALL days (9 case-day combinations):",
        overall.to_string(),
        "",
        "Maximum mismatch per case (largest |sim - analytical| across all days/depths):",
        worst_points.to_string(index=False),
        "",
        "Metric definitions:",
        "  N                : number of paired analytical depths",
        "  RMSE             : root mean squared error (sim - analytical)",
        "  MAE              : mean absolute error",
        "  MaxAbsError      : maximum absolute error across the profile",
        "  MBE              : mean bias error (positive = numerical overshoots)",
        "  NRMSE_%          : RMSE normalized by analytical range, expressed as %",
        "  R2               : Pearson coefficient of determination",
        "  NSE              : Nash-Sutcliffe efficiency (1.0 = perfect match)",
        "  Pooled_RMSE      : sqrt(sum(N_i * RMSE_i^2) / sum(N_i)), weighted by N",
        "  Max_AbsError     : largest |error| seen for the case across DAY 1, 2, 3",
        "  Max_AbsError_DAY : the day on which Max_AbsError occurred",
        bar,
    ]
    return "\n".join(lines)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    xlsx_path = os.path.join(here, INPUT_FILE)
    out_path = os.path.join(here, OUTPUT_FILE)
    txt_path = os.path.join(here, TXT_OUTPUT_FILE)

    summary_frames = []
    paired_frames = []

    for case in CASES:
        summary, paired = evaluate_case(xlsx_path, case)
        summary_frames.append(summary)
        paired_frames.append(paired)

    summary_all = pd.concat(summary_frames, ignore_index=True)
    paired_all = pd.concat(paired_frames, ignore_index=True)

    pd.set_option("display.float_format", lambda v: f"{v:.6g}")
    agg = summary_all.groupby("CASE").apply(
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

    # Locate the single worst point (largest absolute error) for each case.
    worst_idx = paired_all.groupby("CASE")["ABS_ERROR"].idxmax()
    worst_points = paired_all.loc[worst_idx, [
        "CASE", "DAY", "Y", "CONC_RATIO_ANALYTICAL",
        "CONC_RATIO_SIMULATED_INTERP", "ABS_ERROR",
    ]].reset_index(drop=True)

    # Overall summary across all cases and days.
    overall = pd.Series({
        "Mean_RMSE": summary_all["RMSE"].mean(),
        "Pooled_RMSE": np.sqrt(
            (summary_all["RMSE"] ** 2 * summary_all["N"]).sum()
            / summary_all["N"].sum()
        ),
        "Mean_MAE": summary_all["MAE"].mean(),
        "Max_AbsError": summary_all["MaxAbsError"].max(),
        "Mean_R2": summary_all["R2"].mean(skipna=True),
        "Mean_NSE": summary_all["NSE"].mean(skipna=True),
    }, name="ALL_CASES_ALL_DAYS")

    report = build_report(summary_all, agg, worst_points, overall)
    print(report)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(report + "\n")

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        summary_all.to_excel(writer, sheet_name="METRICS_SUMMARY", index=False)
        agg.to_excel(writer, sheet_name="METRICS_AGGREGATE")
        overall.to_frame().T.to_excel(writer, sheet_name="METRICS_OVERALL", index=False)
        worst_points.to_excel(writer, sheet_name="WORST_POINT_PER_CASE", index=False)
        paired_all.to_excel(writer, sheet_name="PAIRED_POINTWISE", index=False)

    print(f"\nWrote text report to: {txt_path}")
    print(f"Wrote Excel results to: {out_path}")


if __name__ == "__main__":
    main()
