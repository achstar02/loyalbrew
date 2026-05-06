@echo off
chcp 65001 >nul
echo ============================================
echo   LoyalBrew Local Dev Server
echo   Starting HTTP server on http://localhost:8080
echo ============================================
echo.
echo Press Ctrl+C to stop the server
echo.

:: Try Python first, then Node.js, then PHP
python -m http.server 8080 --bind 127.0.0.1 2>nul && goto :end

echo [!] Python not found, trying Node.js...
npx -y http-server -p 8080 -c-1 --cors 2>nul && goto :end

echo [!] Node.js not found, trying PHP...
php -S localhost:8080 2>nul && goto :end

echo [ERROR] No Python/Node.js/PHP found. Please install one of them.
pause
exit /b 1

:end
