$lines = Get-Content 'C:\Users\Administrator\CodeBuddy\20260416214625\app.js' -Encoding UTF8

# Direct check: extract just the mItemRemoved portion
Write-Host "=== ZH mItemRemoved (line 3948) ==="
$line3948 = $lines[3947]
$idx = $line3948.IndexOf("mItemRemoved")
$snippet = $line3948.Substring($idx)
Write-Host $snippet

Write-Host ""
Write-Host "=== MS mItemRemoved (line 4035) ==="
$line4035 = $lines[4034]
$idx = $line4035.IndexOf("mItemRemoved")
$snippet = $line4035.Substring($idx)
Write-Host $snippet

Write-Host ""
Write-Host "=== TA mItemRemoved (line 4122) ==="
$line4122 = $lines[4121]
$idx = $line4122.IndexOf("mItemRemoved")
$snippet = $line4122.Substring($idx)
Write-Host $snippet
