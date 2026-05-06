$lines = Get-Content 'C:\Users\Administrator\CodeBuddy\20260416214625\app.js' -Encoding UTF8

# Check mt() function
Write-Host "=== mt() function ==="
for ($ix = 0; $ix -lt $lines.Count; $ix++) {
    if ($lines[$ix] -match 'function mt\(') {
        for ($j = $ix; $j -lt $ix + 5 -and $j -lt $lines.Count; $j++) {
            Write-Host "$($j+1): $($lines[$j])"
        }
        break
    }
}

# Check _merchantLang initialization
Write-Host ""
Write-Host "=== _merchantLang initialization ==="
for ($ix = 0; $ix -lt $lines.Count; $ix++) {
    if ($lines[$ix] -match '_merchantLang\s*=') {
        Write-Host "$($ix+1): $($lines[$ix])"
    }
}

# Check if MERCHANT_LANGS.ta is somehow overriding others
Write-Host ""
Write-Host "=== MERCHANT_LANGS structure check ==="
$inTA = $false
$taStart = 0
for ($ix = 0; $ix -lt $lines.Count; $ix++) {
    if ($lines[$ix] -match '^\s*ta\s*:\s*\{' -and $ix -gt 3855) {
        $taStart = $ix
        Write-Host "TA block starts at line $($ix+1)"
        # Check if there's a syntax error that causes TA to override
        for ($j = $ix; $j -lt $ix + 10 -and $j -lt $lines.Count; $j++) {
            if ($lines[$j] -match '^\s*\}\s*,?\s*$') {
                Write-Host "TA block ends at line $($j+1)"
                break
            }
        }
        break
    }
}
