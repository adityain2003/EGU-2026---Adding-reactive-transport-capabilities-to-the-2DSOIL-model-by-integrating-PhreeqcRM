# EGU 2026 — Adding reactive-transport capabilities to the 2DSOIL model by integrating PhreeqcRM

Companion repository for the EGU 2026 conference presentation. It contains
self-contained codebases that exercise a coupled **2DSOIL ↔ PhreeqcRM**
reactive-transport model and verify it against independent references —
analytical solutions for simple kinetics, PHREEQC's standalone transport
solver (IPhreeqc) for multi-species cation-exchange columns, and
field-observed nitrogen leaching for a layered kinetic biogeochemistry
study.

The repository is organised as a monorepo. Each top-level numbered folder
is one self-contained study / codebase, with its own modified Fortran glue,
its own `.pqi` chemistry inputs, and its own pre-built binaries.

```
.
├── 1_BENCHMARKING_STUDY/         codebase 1: analytical-solution benchmark
│                                 (3 cases: conservative, 1st-order decay,
│                                 1st-order decay + 0-order production)
├── 2_CATION_EXCHANGE_PROBLEM/    codebase 2: 5-species cation-exchange
│                                 column (Ca / Cl / Na / K / NO3) with
│                                 exchanger X, benchmarked against IPhreeqc
└── 3_NITRATE_LEACHING/           codebase 3: Murphy sand N leaching, 8-layer
                                  × 50-cell column with first-order kinetics
                                  for organic-N → NH4 → NO3 → N2O across 7
                                  scenarios (NR / ZK / ZK_ND / FK / FK_ND /
                                  CK / CK_ND), benchmarked against field-
                                  observed leaching data
```

> **Important:** the three codebases share a directory layout, but the
> Fortran glue (`PhreeqcRM.FOR`, `FERTIGATION.FOR`, `2DMAIZSIM.FOR`),
> the `.pqi` chemistry inputs, and the post-processing scripts are
> **different** — do not assume something in `2_…/` works the same way
> as in `1_…/`, or that `3_…/` matches either of them.

---

## 1_BENCHMARKING_STUDY — analytical-solution benchmark

Three exercises were performed against analytical references:

| # | Scenario                                 | Reaction terms                              |
|---|------------------------------------------|---------------------------------------------|
| 1 | Conservative transport (no reaction)     | none                                        |
| 2 | First-order decay of species A           | μ = 3 × 10⁻⁶ mol/sec                        |
| 3 | First-order decay + zero-order production| μ = 3 × 10⁻⁶ mol/sec, γ = 1 × 10⁻⁶ mol/sec  |

For Cases 2 and 3, μ (decay rate) and γ (zero-order production) are set in
the visualization / error-calculation Python scripts.

### Layout

```
1_BENCHMARKING_STUDY/
├── INFO.txt
├── ANALYSIS_AND_FIGURES/                                 Analytical-solution scripts, error metrics, and figures
│   └── FIGURES/                                          Per-case and combined publication figures
└── Maizsim_PhreeqcRM/
    ├── soil source/      2DSOIL (Fortran)  → builds 2dMAIZSIM.exe
    ├── crop source/      MAIZSIM (C++)     → builds Maizsim.dll
    ├── PHREEQCRM/        PhreeqcRM library source (vendored, USGS)
    ├── PHREEQCRM_BUILD/  CMake / MSBuild outputs for PhreeqcRM (.dll, .lib, databases)
    ├── TEST_CASE/        Sample scenario inputs
    └── maizsim07_PHREEQCRM.sln
```

### Components

- **2DSOIL** — Fortran finite-element soil-water/solute solver.
- **MAIZSIM** — C++ crop model, linked as a DLL.
- **PhreeqcRM** — USGS reactive-transport library (`PhreeqcRM.dll`).
- The Fortran ↔ C++ bridge to PhreeqcRM lives in
  `soil source/PhreeqcRM.FOR` and `soil source/RM_interface.F90`.

### Pre-built binaries

So the model can run on a target Windows x64 PC without rebuilding,
the following are checked in:

- `Maizsim_PhreeqcRM/soil source/x64/Debug/2dMAIZSIM.exe`
- `Maizsim_PhreeqcRM/soil source/x64/Debug/Maizsim.dll`
- `Maizsim_PhreeqcRM/soil source/x64/Debug/PhreeqcRM.dll`, `PhreeqcRMd.dll`
- `Maizsim_PhreeqcRM/PHREEQCRM_BUILD/{Debug,Release}/PhreeqcRM*.{dll,lib,exp}`
- PHREEQC chemistry databases (`*.dat`) under
  `Maizsim_PhreeqcRM/PHREEQCRM_BUILD/database/`

### Inputs and outputs (run-time files in `soil source/x64/Debug/`)

| File                          | Role                                                                 |
|-------------------------------|----------------------------------------------------------------------|
| `PHREEQCRM_FILENAME.txt`      | Input: name of the active `.pqi` chemistry runfile (Case 1 / 2 / 3). |
| `PHREEQCRM_RUNFILE_BENCHMARKING_CASE_{1,2,3}.pqi` | PhreeqcRM chemistry definitions per case.        |
| `FERTIGATION_SCHEDULE.txt`    | Input: dates / hours / solute-flux / water-flux for fertigation.     |
| `phreeqc.dat`, `Amm.dat`, `Amm_2DSOIL.dat` | PHREEQC thermodynamic databases.                        |
| `run.dat`, `runTEST_CASE_1.dat` | 2DSOIL run controllers.                                            |
| `TEST_CASE_BM/`, `TEST_CASE_BM_750CM/` | Soil and climate inputs for the benchmark grids.            |
| **`FERTIGATION_OUTPUT.txt`**  | **Main output** — concentrations of species A at every node where x = 0 (1-D profile), written at hour 0 of each day. |
| `PHREEQC_SPECIES_OUT.txt`     | PhreeqcRM species-concentration dump.                                |
| `PHREEQCRM_2DSOIL.chem.txt`, `PHREEQCRM_2DSOIL.log.txt` | PhreeqcRM-side chemistry / log output.      |

The `FERTIGATION_OUTPUT.txt` write is in
`soil source/FERTIGATION.FOR` (subroutine `FERTIGATION`, near line 124).
Columns: `NODE_NUM, TIME, DATE, HOUR, X, Y, CONC`.

### Run scenario

Per `INFO.txt`:

- **Days 1–5 (1–5 Jan 2024)** — media saturates, no solute applied.
- **Day 6 onwards** — solute is injected via the fertigation module; species A
  concentrations are written to `FERTIGATION_OUTPUT.txt` at hour 0 of each day.

### Analytical solutions, error metrics, and figures

All consolidated under `1_BENCHMARKING_STUDY/ANALYSIS_AND_FIGURES/`. The pipeline
evaluates each case's 1-D analytical solution at the **same 437-node depth
grid as the simulated profile** (no interpolation), writes the result back to
`RESULTS_BENCHMARKING_ANALYTICAL_SOLUTION_750CM.xlsx` as
`CONC_RATIO_ANALYTICAL_AT_Y_DAY_k` columns, then computes errors and produces
publication figures.

Run order:

1. `ANALYTICAL_AT_SIMULATED_DEPTHS_CASE_1.py` — Case 1, Ogata-Banks (1961)
   advection-dispersion. Adds 4 columns to the `CASE_1` sheet, saves a
   single-panel "(a)" figure to `FIGURES/`.
2. `ANALYTICAL_AT_SIMULATED_DEPTHS_CASE_2.py` — Case 2, van Genuchten (1981)
   with first-order decay (`mu = 0.2592 1/day`, `gamma = 0`). Adds 4 columns
   to `CASE_2`, saves "(b)" figure.
3. `ANALYTICAL_AT_SIMULATED_DEPTHS_CASE_3.py` — Case 3, full van Genuchten
   (`mu = 0.2592`, `gamma = 0.0864 1/day`). Adds 4 columns to `CASE_3`,
   saves "(c)" figure.
4. `ERROR_CALCULATION.py` — reads the new dense columns, computes per-day
   RMSE / MAE / MaxAbsError / MBE / NRMSE / R² / NSE on N=437 paired depths,
   plus per-case and overall aggregates (Mean / Pooled / Simple RMSE and
   Mean NRMSE_%). Outputs `RESULTS_BENCHMARKING_ERROR_METRICS.{txt,xlsx}`.
5. `PHREEQC_BENCHMARKING_COMBINED_FIGURE.py` — 3-panel publication figure
   (a) (b) (c), saved to `FIGURES/` in PNG (300/600 DPI), PDF, SVG, and EPS.

Steps 4 and 5 depend on step 1-3 having run; they're independent of each
other.

---

## 2_CATION_EXCHANGE_PROBLEM — multi-species cation-exchange column

A column-displacement / cation-exchange study in the spirit of PHREEQC's
classic *Example 11*: a soil column initially equilibrated with a Na–K–NO₃
solution (in equilibrium with an exchanger `X`) is flushed from the top
with a Ca–Cl solution. The exchanger releases Na⁺/K⁺, retains Ca²⁺, and the
five solutes (Ca²⁺, Cl⁻, Na⁺, K⁺, NO₃⁻) develop characteristic breakthrough
profiles down the column.

The 2DSOIL ↔ PhreeqcRM result is benchmarked **against IPhreeqc** (PHREEQC's
standalone transport solver) running the same chemistry on the same grid —
not against an analytical solution. Reference output files live in
`IPHREEQC_FILES/` as `IPHREEQC_OUTPUT_*.sel` and the combined comparison
spreadsheets `RESULTS_100cm_1cm*.xlsx`.

### Layout

```
2_CATION_EXCHANGE_PROBLEM/
├── ANALYSIS_AND_FIGURES/                    Error metrics + publication figures
│   └── FIGURES/                             CATIONS / ANIONS publication figures
├── IPHREEQC_FILES/                          PHREEQC standalone reference (inputs + .sel outputs)
└── Maizsim_PhreeqcRM/                       2DSOIL + MAIZSIM + PhreeqcRM (modified glue)
    ├── soil source/      2DSOIL (Fortran) — see "Differences from codebase 1" below
    ├── crop source/      MAIZSIM (C++)
    ├── PHREEQCRM/        PhreeqcRM library source (vendored)
    ├── PHREEQCRM_BUILD/  built DLLs / LIBs / databases
    └── maizsim07_PHREEQCRM.sln
```

### Chemistry (`PHREEQCRM_RUNFILE_CATION_EXCHANGE.pqi`)

| Block             | Contents                                                                |
|-------------------|-------------------------------------------------------------------------|
| `SOLUTION 0`      | Inflow at the top boundary: Ca = 0.0006 mol/L, Cl = 0.0012 mol/L, pH 7. |
| `SOLUTION 1–500`  | Initial column water: Na = 0.001, K = 0.0002, N(5)=NO₃ = 0.0012 mol/L.  |
| `EXCHANGE 0`      | Cation exchanger `X`, total sites 0.0011 eq/L, equilibrated with cell 1; copied to cells 1–500. |
| `SELECTED_OUTPUT` | Writes pH, pe, charge balance, % error, totals (O Ca Cl K N X), Eh.     |

### Differences from `1_BENCHMARKING_STUDY` (do not assume parity)

- **`PhreeqcRM.FOR`** has the runfile **hardcoded** to
  `"PHREEQCRM_RUNFILE_CATION_EXCHANGE.pqi"` (lines 182, 653) — there is
  **no** `PHREEQCRM_FILENAME.txt` in this codebase.
- **`FERTIGATION.FOR`** is the multi-solute version. Solute 2 inflow is
  auto-set to `2 × (35.453 / 40.08) × solute_1` so the Cl⁻ flux balances
  the Ca²⁺ flux on a charge / molar-equivalent basis.
- **Output is now CSV-formatted, sampled at `x = 5.0` cm** (column interior,
  not the surface), at **every step** (the hour-0 filter is commented out).
  Columns: `NODE_NUM, TIME, DATE, HOUR, X, Y, MMOLS_1, … MMOLS_5` where
  `MMOLS_i = Conc(I,i) / MW_i` with MW = 40.08, 35.453, 22.9898, 39.102,
  62.01 for Ca²⁺, Cl⁻, Na⁺, K⁺, NO₃⁻ respectively.
- **`FERTIGATION_SCHEDULE.txt`** uses solute flux 24.0, water flux 1.0 cm/day
  (vs 1000.0 / 5.0 in codebase 1), with three identical fertigation events.
- **`2DMAIZSIM.FOR`** also differs from codebase 1.

### Variant `.pqi` runfiles checked in

In `Maizsim_PhreeqcRM/soil source/x64/Debug/`:

| File                                                       | Purpose                                                  |
|------------------------------------------------------------|----------------------------------------------------------|
| **`PHREEQCRM_RUNFILE_CATION_EXCHANGE.pqi`**                | **Active runfile** (hardcoded in `PhreeqcRM.FOR`).       |
| `PHREEQCRM_RUNFILE_BASIC_KINETICS_27_11_2024.pqi`          | Earlier kinetics-only experiment.                        |
| `PHREEQCRM_RUNFILE_SOLUTIONS_ONLY_26_NOV_2024.pqi`         | Solutions only — no exchanger.                           |
| `PHREEQCRM_RUNFILE_DECOUPLED.pqi`                          | Decoupled / diagnostic variant.                          |
| `PHREEQCRM_RUNFILE_TEST_CASE_SEQ_RXN.pqi`                  | Sequential-reactions test.                               |
| `PHREEQCRM_RUNFILE_BENCHMARKING_STUDY_1.pqi`               | Carry-over from codebase 1 (kept for reference).         |

To switch the active runfile, edit the literal string in
`soil source/PhreeqcRM.FOR` at lines 182 and 653 and rebuild.

### Reference / standalone PHREEQC inputs (in `IPHREEQC_FILES/`)

| File                                       | Purpose                                                                |
|--------------------------------------------|------------------------------------------------------------------------|
| `100cm_1_cm_ALL_NODES.pqi`                 | PHREEQC `TRANSPORT` input: 100 cm column, 1 cm cells, all-node logging.|
| `100cm_1_cm_END_NODE.pqi`                  | Same column but logging only the end node.                             |
| `*.pqi.out`                                | PHREEQC standalone run output.                                         |
| `IPHREEQC_OUTPUT_100cm_1cm*.sel`           | `SELECTED_OUTPUT` files from IPhreeqc — the **reference** to compare against. |
| `ex11adv.sel`, `ex11trn.sel`, `advect.pqi` | PHREEQC manual *Example 11* advection / transport baselines.           |
| `RESULTS_100cm_1cm*.xlsx`                  | Comparison spreadsheets — 2DSOIL-PhreeqcRM and IPhreeqc side-by-side.  |

### Run scenario

The 2DSOIL-PhreeqcRM run uses the same `Maizsim_PhreeqcRM/soil source/x64/Debug/2dMAIZSIM.exe`
binary that codebase 1 uses (rebuilt against the modified Fortran). The
fertigation schedule injects Ca/Cl water at the top of the column for the
duration of the simulation (Jan 2024 dates in `FERTIGATION_SCHEDULE.txt`),
and concentrations at `x = 5.0` cm are written to `FERTIGATION_OUTPUT.txt`
every step in mmol/L for all five species.

### Analysis pipeline + figures

All consolidated under `2_CATION_EXCHANGE_PROBLEM/ANALYSIS_AND_FIGURES/`. Run
via `RUN_ALL.bat` or sequentially:

1. `ERROR_CALCULATION_CATION_EXCHANGE.py` — per-species, per-day RMSE / MAE
   / MaxAE / MBE / NRMSE / R² / NSE / MAPE / SMAPE for all 5 species
   (Ca²⁺, Cl⁻, Na⁺, K⁺, NO₃⁻) over days 1–3, plus per-species, per-group
   (cations vs anions), and overall aggregates (Mean / Pooled / Simple
   RMSE and Mean NRMSE_%). The IPhreeqc reference is
   linearly interpolated from its cell-centered grid (0.5–99.5 cm) onto
   the simulated node grid (0–100 cm) before metrics are computed; values
   ≤ 0.01 mmol/L on either side are masked out (avoid MAPE blow-up).
   Outputs `RESULTS_CATION_EXCHANGE_ERROR_METRICS.{txt,xlsx}`.
2. `CATION_EXCHANGE_VISUALIZATION.py` — produces two publication figures
   in `FIGURES/`: a 3-panel `CATIONS_*` (Ca²⁺/Na⁺/K⁺) and a 2-panel
   `ANIONS_*` (Cl⁻/NO₃⁻), each in PNG (300 + 600 DPI) and vector PDF.
   Style matches the 1-D benchmarking figures (Times New Roman, dashed
   simulated lines, scatter IPhreeqc markers, bold (a)/(b)/(c) corner
   labels, shared bottom legend, rounded RMSE box at the top of each
   panel).

Workbook used by the pipeline: `RESULTS_100cm_1cm_ALL_NODES.xlsx` in the
same folder (a copy of one of the comparison spreadsheets in
`IPHREEQC_FILES/`).

---

## 3_NITRATE_LEACHING — Murphy sand N leaching, kinetic-variant comparison

A field-experiment-benchmarked study of nitrate leaching from a sandy
soil profile under low-frequency irrigation. Eight soil layers (10 cm
each, 80–0 cm depth, 50 cells per layer = 400 cells total) carry a
four-species nitrogen system (organic-N → ammonium → nitrate → nitrous
gas) driven by layer-specific kinetic mineralisation, nitrification,
and denitrification. The 2DSOIL ↔ PhreeqcRM result is benchmarked
**against field-observed leaching data** from the Murphy sand
low-frequency-irrigation experiment — the first codebase in this repo
to use experimental data as its reference (vs analytical solutions in
codebase 1 and IPhreeqc in codebase 2).

Seven kinetic scenarios are compared:

| Code   | Description                                                      |
|--------|------------------------------------------------------------------|
| NR     | No-reaction control (transport only)                             |
| ZK     | Zero-order mineralisation / nitrification / denitrification      |
| ZK_ND  | Zero-order without denitrification                               |
| FK     | First-order mineralisation / nitrification / denitrification     |
| FK_ND  | First-order without denitrification                              |
| CK     | Conditional kinetics (water-content factor on mineralisation)    |
| CK_ND  | Conditional without denitrification                              |

### Layout

```
3_NITRATE_LEACHING/
├── HOW_TO_RUN_2DSOIL-PHREEQCRM.txt
├── PHREEQCRM_RUNFILE_NITRATE_LEACHING_FIRST_ORDER.pqi   Top-level reference copy
├── 2DSOIL-PHREEQCRM_MURPHY_SAND_LF/                     Analysis + per-scenario run dirs
│   ├── NR/, ZK/, ZK_ND/, FK/, FK_ND/, CK/, CK_ND/       Self-contained 2DSOIL run dirs (one per scenario)
│   ├── MASS_BALANCE_PHREEQC_<SCENARIO>.txt              Per-scenario N mass-balance log
│   ├── OBSERVED_DATA.xlsx                               Murphy field observations
│   ├── COMPARISON_OF_RESULTS.xlsx                       Per-scenario RMSE summary
│   ├── PYTHON_MURPHY_SAND_LF_VISUALIZATION_V3.py        Visualization script
│   └── Figure_1/2/3*.png                                Pre-rendered publication figures
└── Maizsim_PhreeqcRM/
    ├── soil source/      2DSOIL (Fortran) — see "Differences from codebases 1/2"
    ├── crop source/      MAIZSIM (C++)
    ├── PHREEQCRM/        PhreeqcRM library source (vendored)
    ├── PHREEQCRM_BUILD/  built DLLs / LIBs / databases
    └── 3_maizsim07_PHREEQCRM.sln                        Note: numeric prefix (codebases 1/2 use the bare name)
```

### Chemistry (`PHREEQCRM_RUNFILE_NITRATE_LEACHING_*.pqi`)

Custom species (no thermodynamic database used — the species are inert
solutes whose totals are tracked through 2DSOIL transport and updated
each step by PhreeqcRM kinetics):

| Species         | GFW (g/mol) | Role                                                              |
|-----------------|-------------|-------------------------------------------------------------------|
| `[ORGANIC_N]`   | 14.01       | Substrate for mineralisation                                      |
| `[AMMONIUM]`    | 18.04       | Mineralisation product, nitrification substrate                   |
| `[NITRATE]`     | 62.01       | Nitrification product, denitrification substrate, leached species |
| `[NITROUS_GAS]` | 44.01       | Denitrification product (gas)                                     |
| `[THETA_VMC]`   | 1.00        | Volumetric water-content tracer (used in conditional rate factors)|

Eight 10-cm layers (indexed bottom-up: layer 1 = 80–70 cm, layer 8 = 10–0 cm),
50 cells per layer (400 cells total). Each layer has its own first-order
rate constants for the three transformations; nitrification rate is uniform
across layers (6.66 × 10⁻⁶ /s in the FK file), while mineralisation and
denitrification rate constants are layer-specific.

### Differences from codebases 1 and 2 (do not assume parity)

- **`PhreeqcRM.FOR`** has the runfile **hardcoded** to
  `"PHREEQCRM_RUNFILE_NITRATE_LEACHING_CONDITIONAL_KINETICS.pqi"` (lines 247
  and 826) — same convention as codebase 2, no `PHREEQCRM_FILENAME.txt`
  driver exists. The pre-built `2dMAIZSIM.exe` therefore reproduces the
  **CK** scenario; switch scenarios by editing the literal at those two
  lines and rebuilding.
- **Leached-N output** is written to `DELHI_MURPHY.G05` (column `N_Leach`)
  per scenario, one G05 per scenario subfolder under
  `2DSOIL-PHREEQCRM_MURPHY_SAND_LF/`. The visualization joins these G05
  files with the per-step PhreeqcRM mass-balance logs to compute cumulative
  leached / nitrified / denitrified / mineral-N curves.
- **Per-scenario run directories** (`NR/`, `ZK/`, `ZK_ND/`, `FK/`, `FK_ND/`,
  `CK/`, `CK_ND/`) under `2DSOIL-PHREEQCRM_MURPHY_SAND_LF/` are each a
  self-contained 2DSOIL working set: `Run.dat`, `Water.dat`,
  `WatMovParam.DAT`, `DELHI_MURPHY*.dat`, `GridGenDll.dll`,
  `createSoilFiles.exe`, `Rosetta.exe`, plus the post-run outputs
  `DELHI_MURPHY.G03 / .G04 / .G05 / .G06 / .G07`.
- **VS solution file** is `3_maizsim07_PHREEQCRM.sln` (numeric prefix);
  codebases 1/2 use the bare `maizsim07_PHREEQCRM.sln`.
- **VS `WorkingDirectory` per-user fix** is required on a fresh clone —
  the `2dMAIZSIM.vfproj.<USER>.user` files are NOT tracked for codebase 3
  (they ARE for codebases 1/2). See "Running the pre-built `2dMAIZSIM.exe`
  → From Visual Studio" below.

### Variant `.pqi` runfiles checked in

In `Maizsim_PhreeqcRM/soil source/x64/Debug/`:

| File                                                                  | Scenario              |
|-----------------------------------------------------------------------|-----------------------|
| `PHREEQCRM_RUNFILE_NITRATE_LEACHING_NO_REACTION.pqi`                  | NR                    |
| `PHREEQCRM_RUNFILE_NITRATE_LEACHING_ZERO_ORDER.pqi`                   | ZK                    |
| `PHREEQCRM_RUNFILE_NITRATE_LEACHING_ZERO_ORDER_NO_DENIT.pqi`          | ZK_ND                 |
| `PHREEQCRM_RUNFILE_NITRATE_LEACHING_FIRST_ORDER.pqi`                  | FK                    |
| `PHREEQCRM_RUNFILE_NITRATE_LEACHING_FIRST_ORDER_NO_DENIT.pqi`         | FK_ND                 |
| **`PHREEQCRM_RUNFILE_NITRATE_LEACHING_CONDITIONAL_KINETICS.pqi`**     | **CK (active)**       |
| `PHREEQCRM_RUNFILE_NITRATE_LEACHING_CONDITIONAL_KINETICS_NO_DENIT.pqi`| CK_ND                 |
| `PHREEQCRM_RUNFILE_NITRATE_LEACHING_FIRST_ORDER_CALIBRATED.pqi`       | Calibrated FK variant |
| `PHREEQCRM_RUNFILE_BASIC_KINETICS_27_11_2024.pqi`                     | Earlier kinetics-only experiment |
| `PHREEQCRM_RUNFILE.pqi`                                               | Generic / template    |

### Reference data (field observations)

In `2DSOIL-PHREEQCRM_MURPHY_SAND_LF/`:

| File                                                  | Purpose                                                                          |
|-------------------------------------------------------|----------------------------------------------------------------------------------|
| `OBSERVED_DATA.xlsx` (sheet `OBSERVED_N_LEACHED_DATA`) | Murphy sand experimental field N-leaching observations                           |
| `MURPHY's SIMULATION_SAND_LOW_FREQUENCY.xlsx`         | Reference simulation / experimental data from the Murphy study                   |
| `COMPARISON_OF_RESULTS.xlsx` (sheet `RMSE`)           | Per-scenario RMSE and side-by-side comparison                                    |
| `RESULT_COMPARISON.docx`                              | Narrative summary of comparison results                                          |
| `MASS_BALANCE_PHREEQC_<SCENARIO>.txt`                 | Time-stepped delta-nitrified, delta-denitrified, residual mineral-N (one/scenario)|

### Run scenario

Per `HOW_TO_RUN_2DSOIL-PHREEQCRM.txt`:

- The PhreeqcRM `.pqi` provides chemistry initialisation and per-step
  kinetics; three rate-law variants (zero / first / conditional) plus
  their no-denitrification counterparts and a no-reaction control.
- 2DSOIL writes nitrate leached at each step to `DELHI_MURPHY.G05`
  (column `N_Leach`) in the scenario subfolder.
- Total leached N for the run is the sum of all per-step `N_Leach`
  values.
- Three water-application events occur on day 1 (WA#1), day 9 (WA#2),
  and day 23 (WA#3) — annotated on Figure 1.

### Analysis pipeline + figures

All consolidated under `2DSOIL-PHREEQCRM_MURPHY_SAND_LF/`. Run via:

```
python PYTHON_MURPHY_SAND_LF_VISUALIZATION_V3.py
```

The script reads:

- `MASS_BALANCE_PHREEQC_<SCENARIO>.txt` for each of the 7 scenarios
- `<SCENARIO>/DELHI_MURPHY.G05` for each of the 7 scenarios
- `OBSERVED_DATA.xlsx` (sheet `OBSERVED_N_LEACHED_DATA`)
- `COMPARISON_OF_RESULTS.xlsx` (sheet `RMSE`)

…and produces three publication figures:

1. **`Figure_1_COMBINED_LEACHING_RESIDUAL_NO3_TIMELINE.png`** — 2-panel
   time-series. (a) Cumulative NO₃-N leached vs day, observed (scatter)
   vs 7 scenarios (lines), with WA#1/2/3 water-application annotations.
   (b) Soil NO₃-N (mineral pool) vs day, all 7 scenarios.
2. **`Figure_2_COMBINED_RESIDUAL_LEACHED_MINERALIZED_DENITRIFIED_FINAL.png`** —
   2-panel bar chart of end-of-run quantities. (a) Stacked bar — leached
   + soil NO₃-N per scenario + observed. (b) Grouped bar — total
   nitrification + total denitrification per scenario + observed.
3. **`Figure_3_RMSE.png`** — Horizontal bar of per-scenario RMSE against
   the observed leaching curve, with a console-printed ranking table.

---

## Running the pre-built `2dMAIZSIM.exe`

All three codebases ship a pre-built executable so you can reproduce the
runs without rebuilding. The executable reads **all of its inputs from the
current working directory** (run controllers, `.pqi` chemistry runfile,
PHREEQC databases, the fertigation schedule, the `TEST_CASE_BM*/` folders,
etc.) and writes its outputs into the same place.

### From a terminal or Explorer

Just launch the exe from inside its own `Debug/` directory:

```bash
# Codebase 1
cd "1_BENCHMARKING_STUDY/Maizsim_PhreeqcRM/soil source/x64/Debug"
./2dMAIZSIM.exe

# Codebase 2
cd "2_CATION_EXCHANGE_PROBLEM/Maizsim_PhreeqcRM/soil source/x64/Debug"
./2dMAIZSIM.exe

# Codebase 3 — runs the CK (conditional-kinetics) scenario by default
cd "3_NITRATE_LEACHING/Maizsim_PhreeqcRM/soil source/x64/Debug"
./2dMAIZSIM.exe
```

(or double-click `2dMAIZSIM.exe` in Explorer — Windows uses the file's parent
folder as CWD, which is what we want).

### From Visual Studio (F5 / Ctrl+F5) — required one-time fix

VS's default debug **Working Directory** is `$(ProjectDir)` — i.e.
`soil source/` — but the inputs and runtime DLLs live one level deeper, in
`$(IntDir)` = `soil source/x64/Debug/`. So an unmodified F5 launch will
fail to find `run.dat`, `phreeqc.dat`, `PHREEQCRM_RUNFILE_*.pqi`,
`FERTIGATION_SCHEDULE.txt`, `TEST_CASE_BM/`, etc.

To fix this **once per fresh clone, per project**:

1. Open the codebase's solution
   (`Maizsim_PhreeqcRM/maizsim07_PHREEQCRM.sln`) in Visual Studio.
2. In Solution Explorer, right-click the **`2dMAIZSIM`** project →
   **Properties**.
3. **Configuration Properties → Debugging → Working Directory** → set to
   `$(IntDir)`.
4. Click OK.

> **Why this isn't already set on a fresh clone**: Intel Fortran writes
> debug-session settings (working directory, command-line args, env vars) to
> a per-user file `2dMAIZSIM.vfproj.<WINDOWS-USERNAME>.user`. Those files
> are excluded by `.gitignore` because they normally contain personal paths
> and would conflict between machines. The `$(IntDir)` setting therefore
> persists locally for you, but doesn't travel with the repo. Each new
> clone needs the one-time fix above.

A terminal / double-click launch (above) does **not** need this fix — the
working-directory issue only affects F5/Ctrl+F5 from inside Visual Studio.

---

## Building from source

Each codebase ships its **own** Visual Studio solution and PhreeqcRM build
folder, because the Fortran sources differ between studies:

- `1_BENCHMARKING_STUDY/Maizsim_PhreeqcRM/maizsim07_PHREEQCRM.sln`
- `2_CATION_EXCHANGE_PROBLEM/Maizsim_PhreeqcRM/maizsim07_PHREEQCRM.sln`
- `3_NITRATE_LEACHING/Maizsim_PhreeqcRM/3_maizsim07_PHREEQCRM.sln` (numeric prefix)

PhreeqcRM has its own build folder `PHREEQCRM_BUILD/` inside each codebase
(CMake-generated VS solution).

Toolchain used:

- Visual Studio 2022 (`v143` platform toolset)
- Intel oneAPI Fortran Compiler (`ifx`) for the 2DSOIL Fortran project
- CMake 3.30 (used to (re)generate each `PHREEQCRM_BUILD/` folder)

The Fortran linker is configured to pick up `maizsim.lib` from the C++
project's output and `PhreeqcRM.lib` from `PHREEQCRM_BUILD/Release/`
(see `soil source/2dMAIZSIM.vfproj`, configuration `Debug|x64`).

### Runtime requirements on the target PC

The shipped EXE is dynamically linked against:

- **Intel Fortran runtime** (`libifcoremd.dll`, `libifportmd.dll`, …) — install
  via the Intel oneAPI HPC Toolkit (or its redistributable runtime package).
- **Microsoft Visual C++ 2015–2022 Redistributable (x64)**.

Both are vendor components and are **not** redistributable through this repo.

---

## License

The vendored PhreeqcRM source under each codebase's
`Maizsim_PhreeqcRM/PHREEQCRM/phreeqcrm-master/` retains its original USGS
license (see that folder's own license / notice files). The 2DSOIL and
MAIZSIM components retain the licenses of their upstream projects.
