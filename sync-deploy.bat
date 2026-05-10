@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   LoyalBrew 一键同步 + 部署工具
echo ========================================
echo.

set "SOURCE=C:\Users\Administrator\CodeBuddy\20260416214625"
set "DEPLOY=%SOURCE%\deploy"

echo [1/4] 同步文件到 deploy 目录...
echo ----------------------------------------

:: 核心部署文件列表（从源码复制到deploy）
set FILES[0]=index.html
set FILES[1]=style.css
set FILES[2]=app.js
set FILES[3]=firebase-init.js
set FILES[4]=security-patch.js
set FILES[5]=tailwindcdn.js

set COUNT=0
for /L %%i in (0,1,5) do (
    if exist "%SOURCE%\!FILES[%%i]!" (
        copy /Y "%SOURCE%\!FILES[%%i]!" "%DEPLOY%\!FILES[%%i]!" >nul
        echo   ✅ !FILES[%%i]!
        set /a COUNT+=1
    ) else (
        echo   ❌ !FILES[%%i]! (未找到)
    )
)

:: 复制目录
if exist "%SOURCE%\menu_photos" (
    xcopy /Y /E /I /Q "%SOURCE%\menu_photos" "%DEPLOY%\menu_photos\" >nul 2>&1
    echo   ✅ menu_photos\
    set /a COUNT+=1
)
if exist "%SOURCE%\dist" (
    xcopy /Y /E /I /Q "%SOURCE%\dist" "%DEPLOY%\\dist\" >nul 2>&1
    echo   ✅ dist\
    set /a COUNT+=1
)

echo.
echo   共同步 %COUNT% 个文件/目录

echo.
echo [2/4] 部署到 Vercel...
echo ----------------------------------------
cd /d "%DEPLOY%"
call vercel --prod --yes 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo   ⚠️ Vercel 部署可能失败，继续 Firebase 部署...
) else (
    echo   ✅ Vercel 部署完成
)

echo.
echo [3/4] 部署到 Firebase Hosting...
echo ----------------------------------------
cd /d "%SOURCE%"
call firebase deploy --only hosting 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo   ❌ Firebase 部署失败
) else (
    echo   ✅ Firebase 部署完成
)

echo.
echo [4/4] 完成！
echo ========================================
echo   Vercel:  https://deploy-eight-rho-95.vercel.app
echo   Firebase: https://loyalbrew-app-2f8c7.web.app
echo ========================================
echo.
echo 请用 Ctrl+F5 硬刷新浏览器查看更新！
pause
