@echo off
REM ====================================================================
REM  Cation-exchange benchmark pipeline - runs both Python scripts in
REM  order. Regenerates the error-metrics report and both publication
REM  figures (CATIONS, ANIONS) in FIGURES\.
REM ====================================================================

setlocal
set MPLBACKEND=Agg
cd /d "%~dp0"

echo.
echo ================================================================
echo  Cation-Exchange Benchmark Pipeline (2DSoil-PhreeqcRM vs IPhreeqc)
echo ================================================================

echo.
echo --- Step 1/2: Error metrics (5 species, days 1-3) ---
python ERROR_CALCULATION_CATION_EXCHANGE.py
if errorlevel 1 goto :error

echo.
echo --- Step 2/2: Publication figures (CATIONS + ANIONS) ---
python CATION_EXCHANGE_VISUALIZATION.py
if errorlevel 1 goto :error

echo.
echo ================================================================
echo  Pipeline complete. Outputs:
echo    - RESULTS_CATION_EXCHANGE_ERROR_METRICS.txt and .xlsx
echo    - FIGURES\CATIONS_300DPI.png  and .pdf  (3-panel: Ca2+, Na+, K+)
echo    - FIGURES\ANIONS_300DPI.png   and .pdf  (2-panel: Cl-, NO3-)
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
