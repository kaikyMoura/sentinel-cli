@echo off
setlocal

set ZIP_NAME=%1
if "%ZIP_NAME%"=="" set ZIP_NAME=my-project.zip

rem
set "SEVENZIP_PATH=C:\Program Files\7-Zip\7z.exe"

echo The files are being zipped...
"%SEVENZIP_PATH%" a %ZIP_NAME% * -xr!node_modules -xr!.next -xr!dist -xr!package-lock.json -xr!yarn.lock -xr!pnpm-lock.yaml -xr!.git

echo.
echo The file %ZIP_NAME% was created successfully!

endlocal
pause