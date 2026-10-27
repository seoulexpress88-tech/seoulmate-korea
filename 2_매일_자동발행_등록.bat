@echo off
chcp 65001 >nul
echo 매일 10:30에 새 영문 글을 웹사이트에 자동 발행하는 윈도우 작업을 등록합니다.
schtasks /create /tn "Seoulmate_Publish" /tr "\"%~dp01_사이트_발행.bat\" auto" /sc daily /st 10:30 /f
if errorlevel 1 (
  echo 실패했어요. 이 파일을 마우스 오른쪽 버튼으로 눌러 "관리자 권한으로 실행" 해 주세요.
) else (
  echo 등록 완료. 해제하려면:  schtasks /delete /tn "Seoulmate_Publish" /f
)
pause
