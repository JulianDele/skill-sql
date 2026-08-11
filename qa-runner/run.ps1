param(
    [Parameter(Mandatory=$true)]
    [string]$SqlFile
)

$scriptPath = Join-Path $PSScriptRoot "runner.py"
python $scriptPath $SqlFile
