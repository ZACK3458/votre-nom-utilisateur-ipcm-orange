<#
Run the unit tests locally in PowerShell.
Usage: ./run_tests.ps1
#>
Write-Host "Running unit tests..."
python -m unittest discover -s tests -v
if ($LASTEXITCODE -eq 0) {
    Write-Host "All tests passed"
} else {
    Write-Host "Some tests failed (exit code $LASTEXITCODE)" -ForegroundColor Red
    exit $LASTEXITCODE
}
