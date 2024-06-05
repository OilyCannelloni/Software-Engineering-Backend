@echo off
setlocal enabledelayedexpansion

rem Function to get IP address for a given network interface
for /f "tokens=2 delims=:" %%A in ('netsh interface ip show config name^="Wi-Fi" ^| findstr /R /C:"IP Address"') do (
    set "wifi_ip=%%A"
    set "wifi_ip=!wifi_ip:~1!"
)

for /f "tokens=2 delims=:" %%A in ('netsh interface ip show config name^="Ethernet" ^| findstr /R /C:"IP Address"') do (
    set "eth_ip=%%A"
    set "eth_ip=!eth_ip:~1!"
)

rem Check Wi-Fi connection
for /f "tokens=*" %%A in ('netsh interface show interface ^| findstr /C:"Wi-Fi"') do (
    if not "%%A"=="Disconnected" (
        echo Wi-Fi:
        echo !wifi_ip!
    )
)

rem Check Ethernet connection
for /f "tokens=*" %%A in ('netsh interface show interface ^| findstr /C:"Ethernet"') do (
    if not "%%A"=="Disconnected" (
        echo Ethernet:
        echo !eth_ip!
    )
)

endlocal
