@echo off
REM ============================================================
REM  Local dev launcher: backend (FastAPI) + frontend (Vite)
REM  All settings come from .env in this folder.
REM  Usage:  run.bat          start both servers (hot reload)
REM          run.bat prod     build React and serve everything from FastAPI (like Render)
REM ============================================================
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0"

REM ---- 1. Make sure .env exists ----
if not exist ".env" (
    echo [setup] .env not found, creating it from .env.example
    copy ".env.example" ".env" >nul
    echo [setup] Edit .env with your real values, then run this again if needed.
)

REM ---- 2. Load .env into this window (skip comments and blank lines) ----
for /f "usebackq eol=# tokens=1,* delims==" %%A in (".env") do (
    if not "%%A"=="" set "%%A=%%B"
)
if not defined API_HOST set "API_HOST=127.0.0.1"
if not defined API_PORT set "API_PORT=8000"
if not defined FRONTEND_PORT set "FRONTEND_PORT=5173"

REM ---- 3. Find Python ----
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (
    where python >nul 2>nul && set "PY=python"
)
if not defined PY (
    echo [error] Python not found. Install it from https://www.python.org/downloads/
    pause
    exit /b 1
)
where npm >nul 2>nul || (
    echo [error] Node.js / npm not found. Install it from https://nodejs.org/
    pause
    exit /b 1
)

REM ---- 4. Python virtual env + dependencies ----
if not exist ".venv\Scripts\python.exe" (
    echo [setup] Creating virtual env in .venv
    %PY% -m venv .venv || (pause & exit /b 1)
)
set "VENV_PY=%~dp0.venv\Scripts\python.exe"

REM Reinstall only when requirements.txt changed
set "REQ_STAMP=.venv\requirements.installed"
fc /b requirements.txt "%REQ_STAMP%" >nul 2>nul
if errorlevel 1 (
    echo [setup] Installing Python packages
    "%VENV_PY%" -m pip install --disable-pip-version-check -q -r requirements.txt || (pause & exit /b 1)
    copy /y requirements.txt "%REQ_STAMP%" >nul
)

REM ---- 5. Frontend dependencies ----
if not exist "frontend\node_modules" (
    echo [setup] Installing frontend packages
    pushd frontend
    call npm install || (popd & pause & exit /b 1)
    popd
)

REM ---- 6. Start ----
if /i "%~1"=="prod" goto prod

echo.
echo  Backend : http://%API_HOST%:%API_PORT%   (docs: /docs if ENABLE_API_DOCS=true)
echo  Frontend: http://localhost:%FRONTEND_PORT%  ^<-- open this
echo  Close the two server windows to stop.
echo.
start "Backend - FastAPI" cmd /k ""%VENV_PY%" -m uvicorn backend.main:app --reload --reload-dir backend --host %API_HOST% --port %API_PORT%"
start "Frontend - Vite" /d "%~dp0frontend" cmd /k npm run dev
timeout /t 4 /nobreak >nul
start "" "http://localhost:%FRONTEND_PORT%"
exit /b 0

:prod
echo [build] Building React app
pushd frontend
call npm run build || (popd & pause & exit /b 1)
popd
echo.
echo  Production-style server: http://%API_HOST%:%API_PORT%
echo.
start "" "http://%API_HOST%:%API_PORT%"
"%VENV_PY%" -m uvicorn backend.main:app --host %API_HOST% --port %API_PORT%
