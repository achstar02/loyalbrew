$lines = Get-Content 'C:\Users\Administrator\CodeBuddy\20260416214625\app.js' -Encoding UTF8
Write-Host "Total lines: $($lines.Count)"

# Verify the 3 comma fixes
Write-Host ""
Write-Host "=== ZH mItemRemoved (should have comma at end) ==="
for ($ix = 3934; $ix -lt 3940; $ix++) {
    Write-Host "$($ix+1): $($lines[$ix])"
}

Write-Host ""
Write-Host "=== MS mItemRemoved (should have comma at end) ==="
for ($ix = 4021; $ix -lt 4027; $ix++) {
    Write-Host "$($ix+1): $($lines[$ix])"
}

Write-Host ""
Write-Host "=== TA mItemRemoved (should have comma at end) ==="
for ($ix = 4108; $ix -lt 4114; $ix++) {
    Write-Host "$($ix+1): $($lines[$ix])"
}

Write-Host ""
Write-Host "=== EN new keys ==="
for ($ix = 255; $ix -lt 263; $ix++) {
    Write-Host "$($ix+1): $($lines[$ix])"
}

Write-Host ""
Write-Host "=== renderMyOrders fix ==="
for ($ix = 3421; $ix -lt 3440; $ix++) {
    Write-Host "$($ix+1): $($lines[$ix])"
}
