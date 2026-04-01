# Windows Task Scheduler registration script
# Run as: powershell -ExecutionPolicy Bypass -File scripts\register_task.ps1

$TaskName   = "LinkedInClaudeCodeScraper"
$ProjectDir = Split-Path -Parent $PSScriptRoot   # scripts/ 의 부모 = 프로젝트 루트
$RunTime    = "09:00"

# 관리자 권한 확인
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]"Administrator")
if (-not $isAdmin) {
    Write-Error "Administrator privileges required. Right-click PowerShell and run as Administrator."
    exit 1
}

$UvCmd = Get-Command uv -ErrorAction SilentlyContinue
if (-not $UvCmd) {
    Write-Error "uv not found. Check PATH."
    exit 1
}
$UvPath = $UvCmd.Source

$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "[*] Removed existing task"
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
    -StartWhenAvailable

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
    -Description "LinkedIn Claude Code daily scraper (09:00)" | Out-Null

Write-Host ""
Write-Host "[OK] Task registered: $TaskName"
Write-Host "     Schedule : daily at $RunTime"
Write-Host "     Directory: $ProjectDir"
Write-Host ""
Write-Host "Check : Get-ScheduledTask -TaskName $TaskName"
Write-Host "Run now: Start-ScheduledTask -TaskName $TaskName"
Write-Host "Remove : Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false"
