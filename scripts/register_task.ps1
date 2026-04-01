# Windows Task Scheduler 등록 스크립트
# 관리자 권한으로 실행: powershell -ExecutionPolicy Bypass -File scripts\register_task.ps1

$TaskName   = "LinkedInClaudeCodeScraper"
$ProjectDir = "C:\Users\bbba2\OneDrive\바탕 화면\링크드인"
$UvPath     = (Get-Command uv -ErrorAction SilentlyContinue)?.Source
$RunTime    = "09:00"

if (-not $UvPath) {
    Write-Error "uv를 찾을 수 없습니다. PATH를 확인하세요."
    exit 1
}

# 기존 태스크 있으면 삭제
if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "[*] 기존 태스크 삭제됨"
}

$Action = New-ScheduledTaskAction `
    -Execute $UvPath `
    -Argument "run python -m scheduler.daily_job_once" `
    -WorkingDirectory $ProjectDir

$Trigger = New-ScheduledTaskTrigger -Daily -At $RunTime

$Settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2) `
    -RestartCount 2 `
    -RestartInterval (New-TimeSpan -Minutes 10) `
    -StartWhenAvailable  # 시각에 PC 꺼져 있었으면 켜지자마자 실행

$Principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Highest

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Principal $Principal `
    -Description "LinkedIn Claude Code 팁 매일 자동 수집 (09:00)" | Out-Null

Write-Host ""
Write-Host "✅ Task Scheduler 등록 완료"
Write-Host "   태스크명: $TaskName"
Write-Host "   실행시각: 매일 $RunTime"
Write-Host "   작업경로: $ProjectDir"
Write-Host ""
Write-Host "확인: Get-ScheduledTask -TaskName '$TaskName'"
Write-Host "수동실행: Start-ScheduledTask -TaskName '$TaskName'"
Write-Host "삭제:   Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false"
