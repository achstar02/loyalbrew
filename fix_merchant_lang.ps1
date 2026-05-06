# Fix merchant section translation issues in index.html

$file = "C:\Users\Administrator\CodeBuddy\20260416214625\index.html"
$lines = Get-Content $file -Encoding UTF8

$changes = @()

# Issue 1: Commission search placeholder - add data-mi18n-ph
# Line 894: <input type="text" id="commission-search" placeholder="Search by name or phone..." oninput="filterCommissions()" />
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match 'id="commission-search"') {
        $old = $lines[$i]
        $new = $old -replace 'placeholder="Search by name or phone\.\.\."', 'placeholder="Search by name or phone..." data-mi18n-ph="mPhSearchMember"'
        if ($new -ne $old) {
            $changes += "Line $($i+1): Added data-mi18n-ph to commission search"
            $lines[$i] = $new
        }
    }
}

# Issue 2: payment-proofs-list empty state needs data-mi18n
# Line 887: <div id="payment-proofs-list"><p style="color:#aaa;text-align:center;padding:16px" data-mi18n="mNoPaymentProofs">No pending payment proofs</p></div>
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match 'id="payment-proofs-list"') {
        $old = $lines[$i]
        # Check if it already has data-mi18n
        if ($old -notmatch 'data-mi18n=') {
            $new = $old -replace '>', ' data-mi18n="mNoPaymentProofs">'
            $new = $new -replace '<p style="color:#aaa;text-align:center;padding:16px">', '<p style="color:#aaa;text-align:center;padding:16px">'
            $changes += "Line $($i+1): Added data-mi18n to payment-proofs-list container"
            $lines[$i] = $new
        }
    }
}

# Issue 3: commission-records-list empty state - needs to be populated by JS
# The empty state is handled by JS in app.js lines 1891

# Issue 4: Check for other hardcoded English placeholders in merchant section
for ($i = 500; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match 'placeholder="[^"]*"' -and $lines[$i] -notmatch 'data-mi18n-ph=') {
        $placeholder = [regex]::Match($lines[$i], 'placeholder="([^"]*)"').Groups[1].Value
        if ($placeholder -match '[A-Za-z]') {
            $changes += "Line $($i+1): Hardcoded placeholder: `"$placeholder`" - needs data-mi18n-ph"
        }
    }
}

# Write changes
$lines | Set-Content $file -Encoding UTF8

Write-Host "Changes applied:"
$changes | ForEach-Object { Write-Host $_ }
