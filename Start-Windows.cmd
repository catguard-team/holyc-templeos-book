@echo off
setlocal
set PYTHONUTF8=1
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
  py -3 tools\launch.py %*
) else (
  python tools\launch.py %*
)
set "BOOK_EXIT=%ERRORLEVEL%"
if not "%BOOK_EXIT%"=="0" (
  echo.
  echo See docs\PLATFORMS.md for Python and QEMU installation.
  pause
)
exit /b %BOOK_EXIT%
