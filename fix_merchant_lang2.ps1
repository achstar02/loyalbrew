# Fix all merchant translation issues in index.html
$file = "C:\Users\Administrator\CodeBuddy\20260416214625\index.html"
$lines = Get-Content $file -Encoding UTF8

$changes = @()

# Fix 1: Line 894 - commission search placeholder missing data-mi18n-ph
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match 'id="commission-search"') {
        $old = $lines[$i]
        $new = $old -replace 'placeholder="Search by name or phone\.\.\."', 'placeholder="Search by name or phone..." data-mi18n-ph="mPhSearchMember"'
        if ($new -ne $old) {
            $changes += "FIXED Line $($i+1): Added data-mi18n-ph to commission-search"
            $lines[$i] = $new
        }
    }
}

# Fix 2: Line 1154 - complaint-desc placeholder
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match 'id="complaint-desc"') {
        $old = $lines[$i]
        $new = $old -replace 'placeholder="Please describe your issue in detail\.\.\."', 'placeholder="Please describe your issue in detail..." data-mi18n-ph="mPhComplaintDesc"'
        if ($new -ne $old) {
            $changes += "FIXED Line $($i+1): Added data-mi18n-ph to complaint-desc"
            $lines[$i] = $new
        }
    }
}

# Fix 3: Line 1168 - complaint-order-id placeholder
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match 'id="complaint-order-id"') {
        $old = $lines[$i]
        $new = $old -replace 'placeholder="e\.g\. ORD123456"', 'placeholder="e.g. ORD123456" data-mi18n-ph="mPhComplaintOrderId"'
        if ($new -ne $old) {
            $changes += "FIXED Line $($i+1): Added data-mi18n-ph to complaint-order-id"
            $lines[$i] = $new
        }
    }
}

# Fix 4: Line 1217 - complaint-response-text placeholder
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match 'id="complaint-response-text"') {
        $old = $lines[$i]
        $new = $old -replace 'placeholder="Enter your response\.\.\."', 'placeholder="Enter your response..." data-mi18n-ph="mPhComplaintResponse"'
        if ($new -ne $old) {
            $changes += "FIXED Line $($i+1): Added data-mi18n-ph to complaint-response-text"
            $lines[$i] = $new
        }
    }
}

$lines | Set-Content $file -Encoding UTF8

$changes | ForEach-Object { Write-Host $_ }
