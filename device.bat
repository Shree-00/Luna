
@REM @echo off
@REM echo Disconnecting old connections...
@REM adb disconnect
@REM echo Setting up connected device
@REM adb tcpip 5555
@REM echo Waiting for device to initialize
@REM timeout 3
@REM FOR /F "tokens=2" %%G IN ('adb shell ip addr show wlan0 ^|find "inet "') DO set ipfull=%%G
@REM FOR /F "tokens=1 delims=/" %%G in ("%ipfull%") DO set ip=%%G
@REM echo Connecting to device with IP %ip%...
@REM adb connect %ip%

@REM @echo off

@REM rem Set the IP address of your Android device
@REM set DEVICE_IP=192.168.70.79

@REM rem Set the port number for ADB
@REM set ADB_PORT=5555

@REM rem Set the path to the ADB executable
@REM set ADB_PATH="C:\platform-tools\adb.exe"

@REM rem Restart the ADB server
@REM %ADB_PATH% kill-server
@REM %ADB_PATH% start-server

@REM rem Connect to the Android device over Wi-Fi
@REM %ADB_PATH% connect %DEVICE_IP%:%ADB_PORT%


@echo off
setlocal enabledelayedexpansion

@REM updated code
:: Configuration - UPDATE THESE VALUES
set DEVICE_IP=192.168.70.79
set ADB_PORT=5555
set ADB_PATH="C:\platform-tools\adb.exe"

:: Restart ADB Server
echo Restarting ADB service...
%ADB_PATH% kill-server >nul 2>&1
%ADB_PATH% start-server
if errorlevel 1 (
    echo Failed to start ADB server!
    exit /b 1
)

:: Initialize Connection
echo Disconnecting old connections...
%ADB_PATH% disconnect >nul

echo Setting TCP/IP mode...
%ADB_PATH% tcpip %ADB_PORT%
timeout 2 >nul

echo Connecting to %DEVICE_IP%:%ADB_PORT%...
%ADB_PATH% connect %DEVICE_IP%:%ADB_PORT%

:: Verify connection
%ADB_PATH% devices | findstr "%DEVICE_IP%:%ADB_PORT%" >nul
if errorlevel 1 (
    echo Connection failed!
    exit /b 1
)

echo Successfully connected to %DEVICE_IP%:%ADB_PORT%
exit /b 0