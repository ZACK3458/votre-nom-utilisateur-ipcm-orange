<#
Loop local maintenance: format, lint, run tests.
Usage: ./run_local_maintenance.ps1
#>
while ($true) {
    Write-Host "Running local maintenance pass: $(Get-Date)"
    python -m pip install --upgrade pip
    if (Test-Path requirements-dev.txt) { pip install -r requirements-dev.txt }
    python -c "import pkgutil; exit(0 if pkgutil.find_loader('ruff') else 1)" ; if ($LASTEXITCODE -eq 0) { ruff format . ; ruff check . --fix }
    python -c "import pkgutil; exit(0 if pkgutil.find_loader('black') else 1)" ; if ($LASTEXITCODE -eq 0) { black . }
    python -m unittest discover -s tests -v
    Start-Sleep -Seconds 3600
}
