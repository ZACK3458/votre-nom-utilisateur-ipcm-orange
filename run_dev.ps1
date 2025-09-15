# Quick start script for Windows PowerShell
$env:FLASK_ENV = "development"
$python = "C:/orange/venv/Scripts/python.exe"
if (-Not (Test-Path $python)) {
  $python = "python"
}
& $python "c:/orange/run.py"