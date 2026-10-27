@echo off
chcp 65001 >nul
echo Registering a daily Windows task: publishes new English posts to the website every day at 10:30.
powershell -NoProfile -ExecutionPolicy Bypass -Command "$d='%~dp0'.TrimEnd('\'); $a=New-ScheduledTaskAction -Execute 'cmd.exe' -Argument ('/c \"\"'+$d+'\1_사이트_발행.bat\" auto\"') -WorkingDirectory $d; $t=New-ScheduledTaskTrigger -Daily -At 10:30; $s=New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries; Register-ScheduledTask -TaskName 'Seoulmate_Publish' -Action $a -Trigger $t -Settings $s -Force | Out-Null"
if errorlevel 1 (
  echo Failed. Right-click this file and choose "Run as administrator".
) else (
  echo Done. To remove later:  schtasks /delete /tn "Seoulmate_Publish" /f
)
pause
