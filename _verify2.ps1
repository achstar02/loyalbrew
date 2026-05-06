$lines = Get-Content 'C:\Users\Administrator\CodeBuddy\20260416214625\app.js' -Encoding UTF8

# Verify mItemRemoved has comma
Write-Host "=== mItemRemoved lines (should end with comma) ==="
for ($ix = 0; $ix -lt $lines.Count; $ix++) {
    if ($lines[$ix] -match 'mItemRemoved') {
        # Check if the line after mItemRemoved value has a comma
        $line = $lines[$ix]
        $afterRemoved = $line -replace ".*mItemRemoved:\s*'", ""
        $hasComma = $afterRemoved -match "',\s"
        Write-Host "$($ix+1): [comma=$hasComma] $($lines[$ix])"
    }
}

Write-Host ""
Write-Host "=== renderMyOrders statusLabels ==="
for ($ix = 0; $ix -lt $lines.Count; $ix++) {
    if ($lines[$ix] -match 'statusLabels') {
        Write-Host "$($ix+1): $($lines[$ix])"
    }
}

Write-Host ""
Write-Host "=== renderMyOrders typeTag ==="
for ($ix = 0; $ix -lt $lines.Count; $ix++) {
    if ($lines[$ix] -match 'orderTypeTakeaway|orderTypeTable') {
        Write-Host "$($ix+1): $($lines[$ix])"
    }
}
