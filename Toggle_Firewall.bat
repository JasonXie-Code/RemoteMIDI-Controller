@echo off
chcp 65001 >nul
rem 检查公用网络防火墙状态
netsh advfirewall show publicprofile | findstr /C:"State" | findstr /C:"ON" >nul
if %errorlevel% equ 0 (
    rem 公用网络防火墙当前处于开启状态，将其关闭
    netsh advfirewall set publicprofile state off
    echo 公用网络防火墙已关闭。
) else (
    rem 公用网络防火墙当前处于关闭状态，将其开启
    netsh advfirewall set publicprofile state on
    echo 公用网络防火墙已开启。
)

rem 检查专用网络防火墙状态
netsh advfirewall show privateprofile | findstr /C:"State" | findstr /C:"ON" >nul
if %errorlevel% equ 0 (
    rem 专用网络防火墙当前处于开启状态，将其关闭
    netsh advfirewall set privateprofile state off
    echo 专用网络防火墙已关闭。
) else (
    rem 专用网络防火墙当前处于关闭状态，将其开启
    netsh advfirewall set privateprofile state on
    echo 专用网络防火墙已开启。
)

pause    