# All-in-one automation script for Windows PowerShell
# - Installs deps
# - Runs tests
# - Starts Flask app
# - Optionally commits and pushes changes

$ErrorActionPreference = "Stop"

function Get-Python {
  $p = "C:/orange/venv/Scripts/python.exe"
  if (-Not (Test-Path $p)) { return "python" }
  return $p
}

function Install-Deps {
  $py = Get-Python
  & $py -m pip install --upgrade pip > $null 2>&1
  & $py -m pip install -r C:/orange/requirements.txt > $null 2>&1
}

function Invoke-Tests {
  $py = Get-Python
  & $py -m unittest discover -s C:/orange/tests -v
}

function Start-App {
  $py = Get-Python
  Start-Process -FilePath $py -ArgumentList "C:/orange/run.py" -WindowStyle Hidden
}

function Invoke-AutoCommitPush {
  param(
    [string]$Message = "chore: auto commit by auto_all.ps1"
  )
  git add -A
  if (-Not (git diff --cached --quiet)) {
    git commit -m $Message
    git push
  }
}

Write-Host "Installing dependencies..."
Install-Deps

Write-Host "Running tests..."
Invoke-Tests

Write-Host "Starting Flask app in background..."
Start-App

param(
  [switch]$Push
)
if ($Push) {
  Write-Host "Auto committing and pushing changes..."
  Invoke-AutoCommitPush
}

Write-Host "Done. App is running."
