@echo off
setlocal

cd /d "%~dp0"

echo ======================================
echo Iniciando ERP Loja de Carros
echo ======================================
echo.

echo Pasta atual:
echo %CD%
echo.

if not exist "python\python.exe" (
    echo ERRO: nao encontrei python\python.exe
    echo A pasta python precisa estar na mesma pasta deste .bat.
    echo.
    pause
    exit /b 1
)

if not exist "app\manage.py" (
    echo ERRO: nao encontrei app\manage.py
    echo A pasta app precisa estar na mesma pasta deste .bat.
    echo.
    pause
    exit /b 1
)

echo Verificando Python portatil...
python\python.exe --version

if errorlevel 1 (
    echo.
    echo ERRO: o Python portatil nao iniciou.
    echo Talvez voce esteja tentando rodar isso fora do Windows.
    echo.
    pause
    exit /b 1
)

echo.
echo Verificando Django...
python\python.exe -c "import django; print('Django:', django.get_version())"

if errorlevel 1 (
    echo.
    echo ERRO: Django nao foi encontrado no Python portatil.
    echo Rode primeiro instalar-erp.bat para instalar as dependencias.
    echo.
    pause
    exit /b 1
)

echo.
echo Aplicando migrations...
cd app
..\python\python.exe manage.py migrate

if errorlevel 1 (
    echo.
    echo ERRO: falha ao aplicar migrations.
    echo.
    pause
    exit /b 1
)

echo.
echo Abrindo navegador...
start "" "http://127.0.0.1:8000/"

echo.
echo Iniciando servidor Django...
echo Para parar o ERP, feche esta janela ou pressione CTRL+C.
echo.

..\python\python.exe manage.py runserver 127.0.0.1:8000

echo.
echo O servidor foi encerrado.
pause
