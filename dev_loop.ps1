# Dev loop: run Flask app and re-run tests on changes (without extra deps)
$ErrorActionPreference = "Stop"

function Start-App {
  $python = "C:/orange/venv/Scripts/python.exe"
  if (-Not (Test-Path $python)) { $python = "python" }
  Start-Process -FilePath $python -ArgumentList "c:/orange/run.py" -WindowStyle Hidden
}

function Invoke-Tests {
  $python = "C:/orange/venv/Scripts/python.exe"
  if (-Not (Test-Path $python)) { $python = "python" }
  & $python -m unittest discover -s C:/orange/tests -v
}

Write-Host "Starting Flask app..."
Start-App

$lastHash = ""
function Get-TreeHash($path) {
  (Get-ChildItem -Recurse -File $path | Get-FileHash -Algorithm SHA256).Hash -join ""
}

Write-Host "Watching for changes... Press Ctrl+C to stop."
while ($true) {
  try {
  $h = Get-TreeHash "C:/orange/app"
    if ($h -ne $lastHash) {
      Write-Host "Changes detected -> Running tests..." -ForegroundColor Yellow
      $lastHash = $h
  Invoke-Tests
    }
    Start-Sleep -Seconds 2
  } catch {
    Write-Warning $_
    Start-Sleep -Seconds 3
  }
}
