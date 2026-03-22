@echo off
:: run_monitor.bat
:: Windows 작업 스케줄러로 매일 07:00 자동 실행
:: 등록 방법: 아래 "등록 방법" 섹션 참조

cd /d C:\infovail-iq
call C:\infovail-iq\.venv\Scripts\activate.bat
python scripts\monitor_events.py >> logs\monitor_events.log 2>&1

:: ── 등록 방법 (PowerShell에서 1회 실행) ──────────────────────────────────────
::
:: $action  = New-ScheduledTaskAction -Execute "C:\infovail-iq\scripts\run_monitor.bat"
:: $trigger = New-ScheduledTaskTrigger -Daily -At "07:00"
:: $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable
:: Register-ScheduledTask -TaskName "Infovail-IQ Monitor" `
::     -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest
::
:: 확인:
:: Get-ScheduledTask -TaskName "Infovail-IQ Monitor"
::
:: 수동 실행 테스트:
:: Start-ScheduledTask -TaskName "Infovail-IQ Monitor"
