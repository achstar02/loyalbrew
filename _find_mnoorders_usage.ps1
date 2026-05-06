$lines = Get-Content 'C:\Users\Administrator\CodeBuddy\20260416214625\app.js' -Encoding UTF8

Write-Host "=== All lines with mNoOrdersFound ==="
for ($ix = 0; $ix -lt $lines.Count; $ix++) {
    if ($lines[$ix] -match 'mNoOrdersFound') {
        Write-Host "$($ix+1): $($lines[$ix])"
    }
}
