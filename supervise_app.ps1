<#
Supervise the Flask app: poll /healthz and restart if unresponsive.
Usage: Start-Process -FilePath powershell -ArgumentList '-File','./supervise_app.ps1' -NoNewWindow -PassThru
#>

$appScript = "run.py"
$logFile = "supervisor.log"

function Log($msg) {
    $line = "$(Get-Date -Format o) - $msg"
    $line | Out-File -FilePath $logFile -Append -Encoding utf8
    Write-Host $line
}

function Start-App {
    Log "Starting app via python $appScript"
    Start-Process -NoNewWindow -FilePath python -ArgumentList $appScript -RedirectStandardOutput .\dev_server.log -RedirectStandardError .\dev_server.err -PassThru | Out-Null
    Start-Sleep -Seconds 2
}

function Stop-App {
    $procs = Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object { $_.Path -and (Get-Content $appScript -ErrorAction SilentlyContinue | Select-String -SimpleMatch 'app.run') }
    foreach ($p in $procs) {
        Log "Stopping process Id=$($p.Id) Name=$($p.ProcessName)"
        try { $p | Stop-Process -Force -ErrorAction Stop } catch { Log "Failed to stop $($p.Id): $_" }
    }
}

# Ensure app is running at start
if (-not (Get-Process -Name python -ErrorAction SilentlyContinue)) {
    Start-App
}

$backoff = 5
while ($true) {
    try {
        $resp = Invoke-WebRequest -Uri http://127.0.0.1:5000/healthz -UseBasicParsing -TimeoutSec 5
        if ($resp.StatusCode -eq 200) {
            Log "Health OK"
            $backoff = 5
        } else {
            Log "Health check returned status $($resp.StatusCode). Restarting app."
            Stop-App
            Start-App
            $backoff = [Math]::Min(60, $backoff * 2)
        }
    } catch {
        Log "Health check failed: $_. Restarting app."
        Stop-App
        Start-App
        $backoff = [Math]::Min(60, $backoff * 2)
    }
    Start-Sleep -Seconds $backoff
}
