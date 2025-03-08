@echo off
echo === Cai dat du an MyBlog ===

REM Kiem tra Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python khong duoc tim thay. Vui long cai dat Python truoc.
    echo Tai Python tu https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Kiem tra va cai dat pip
python -m ensurepip --upgrade
python -m pip install --upgrade pip

REM Cai dat thu vien Flask va Werkzeug
echo Dang cai dat thu vien...
python -m pip install flask werkzeug

REM Tao thu muc du an neu chua co
set PROJECT_DIR=E:\flask-tiny-app1
if not exist "%PROJECT_DIR%" (
    mkdir "%PROJECT_DIR%"
    echo Da tao thu muc %PROJECT_DIR%
)

REM Tao thu muc static/uploads
set UPLOADS_DIR=%PROJECT_DIR%\static\uploads
if not exist "%UPLOADS_DIR%" (
    mkdir "%UPLOADS_DIR%"
    echo Da tao thu muc %UPLOADS_DIR%
)

REM Sao chep file nguon (giả sử file nằm cùng thư mục với script)
echo Dang sao chep file nguon...
copy *.html "%PROJECT_DIR%" >nul 2>&1
copy *.py "%PROJECT_DIR%" >nul 2>&1
copy *.json "%PROJECT_DIR%" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Loi khi sao chep file. Vui long kiem tra thu muc nguon.
    pause
    exit /b 1
)

REM Chuyen den thu muc du an va chay ung dung
cd /d "%PROJECT_DIR%"
echo Dang khoi chay ung dung...
start cmd /k python app.py

echo === Cai dat hoan tat! Mo trinh duyet va truy cap http://127.0.0.1:5000 ===
pause