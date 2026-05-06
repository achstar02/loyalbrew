# Add complaint placeholder translations to MERCHANT_LANGS in app.js
$file = "C:\Users\Administrator\CodeBuddy\20260416214625\app.js"
$lines = Get-Content $file -Encoding UTF8

$changes = 0

# EN: Find mPhCardName and add new keys after it
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "MERCHANT_LANGS.en" -or $lines[$i - 1] -match "MERCHANT_LANGS.en") {
        # Find the line with mPhCardName in EN
        if ($lines[$i] -match "mPhCardName.*:") {
            $old = $lines[$i]
            $new = $old -replace "(mPhCardName: '[^']*'),", "`$1, mPhComplaintDesc: 'Please describe your issue in detail...', mPhComplaintOrderId: 'e.g. ORD123456', mPhComplaintResponse: 'Enter your response...',"
            if ($new -ne $old) {
                $lines[$i] = $new
                $changes++
                Write-Host "EN: Line $($i+1) updated"
            }
        }
    }
}

# ZH: Find mPhCardName and add new keys after it
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "MERCHANT_LANGS.zh" -and $lines[$i] -match "mPhCardName") {
        $old = $lines[$i]
        $new = $old -replace "(mPhCardName: '[^']*'),", "`$1, mPhComplaintDesc: '请详细描述您的问题...', mPhComplaintOrderId: '例如 ORD123456', mPhComplaintResponse: '输入您的回复...',"
        if ($new -ne $old) {
            $lines[$i] = $new
            $changes++
            Write-Host "ZH: Line $($i+1) updated"
        }
    }
}

# MS: Find mPhCardName and add new keys after it
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "MERCHANT_LANGS.ms" -and $lines[$i] -match "mPhCardName") {
        $old = $lines[$i]
        $new = $old -replace "(mPhCardName: '[^']*'),", "`$1, mPhComplaintDesc: 'Sila huraikan masalah anda secara terperinci...', mPhComplaintOrderId: 'cth. ORD123456', mPhComplaintResponse: 'Masukkan respons anda...',"
        if ($new -ne $old) {
            $lines[$i] = $new
            $changes++
            Write-Host "MS: Line $($i+1) updated"
        }
    }
}

# TA: Find mPhCardName and add new keys after it
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "MERCHANT_LANGS.ta" -and $lines[$i] -match "mPhCardName") {
        $old = $lines[$i]
        $new = $old -replace "(mPhCardName: '[^']*'),", "`$1, mPhComplaintDesc: 'தயவுசெய்து உங்கள் சிக்கலை விரிவாக விவரிக்கவும்...', mPhComplaintOrderId: 'எ.கா. ORD123456', mPhComplaintResponse: 'உங்கள் பதிலை உள்ளிடவும்...',"
        if ($new -ne $old) {
            $lines[$i] = $new
            $changes++
            Write-Host "TA: Line $($i+1) updated"
        }
    }
}

Write-Host "`nTotal changes: $changes"
$lines | Set-Content $file -Encoding UTF8
