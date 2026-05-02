@echo off
REM ====================================================================
REM  PHREEQC-2DSOIL benchmarking pipeline - runs all 5 Python scripts
REM  in order. Regenerates the analytical columns in the workbook, the
REM  error metrics report, and all figures.
REM
REM  Steps 1-3 must run before steps 4 and 5 (they populate the
REM  CONC_RATIO_ANALYTICAL_AT_Y_DAY_k columns that 4 and 5 read).
REM ====================================================================

setlocal
set MPLBACKEND=Agg
cd /d "%~dp0"

echo.
echo ================================================================
echo  PHREEQC-2DSOIL Benchmarking Pipeline
echo ================================================================

echo.
echo --- Step 1/5: Analytical at simulated depths, CASE_1 (Ogata-Banks) ---
python ANALYTICAL_AT_SIMULATED_DEPTHS_CASE_1.py
if errorlevel 1 goto :error

echo.
echo --- Step 2/5: Analytical at simulated depths, CASE_2 (decay) ---
python ANALYTICAL_AT_SIMULATED_DEPTHS_CASE_2.py
if errorlevel 1 goto :error

echo.
echo --- Step 3/5: Analytical at simulated depths, CASE_3 (decay+production) ---
python ANALYTICAL_AT_SIMULATED_DEPTHS_CASE_3.py
if errorlevel 1 goto :error

echo.
echo --- Step 4/5: Error metrics (RMSE / MAE / NSE / R^2 / etc.) ---
python ERROR_CALCULATION.py
if errorlevel 1 goto :error

echo.
echo --- Step 5/5: Combined 3-panel publication figure ---
python PHREEQC_BENCHMARKING_COMBINED_FIGURE.py
if errorlevel 1 goto :error

echo.
echo ================================================================
echo  Pipeline complete. Outputs:
echo    - RESULTS_BENCHMARKING_ANALYTICAL_SOLUTION_750CM.xlsx (updated)
echo    - RESULTS_BENCHMARKING_ERROR_METRICS.txt and .xlsx
echo    - FIGURES\ (per-case panels + combined figure, PNG/PDF/SVG/EPS)
echo ================================================================
echo.
pause
exit /b 0

:error
echo.
echo ================================================================
echo  ERROR: pipeline failed at the previous step. See output above.
echo ================================================================
echo.
pause
exit /b 1
