# Add complaint placeholder translations to MERCHANT_LANGS in app.js
$file = "C:\Users\Administrator\CodeBuddy\20260416214625\app.js"
$lines = Get-Content $file -Encoding UTF8

# EN: line 3907
$old = $lines[3906]
$new = $old -replace "(mPhCardName: '[^']*'),", "`$1, mPhComplaintDesc: 'Please describe your issue in detail...', mPhComplaintOrderId: 'e.g. ORD123456', mPhComplaintResponse: 'Enter your response...',"
$lines[3906] = $new
Write-Host "EN updated: $new"

# ZH: line 3994
$old = $lines[3993]
$new = $old -replace "(mPhCardName: '[^']*'),", "`$1, mPhComplaintDesc: '请详细描述您的问题...', mPhComplaintOrderId: '例如 ORD123456', mPhComplaintResponse: '输入您的回复...',"
$lines[3993] = $new
Write-Host "ZH updated: $new"

# MS: line 4081
$old = $lines[4080]
$new = $old -replace "(mPhCardName: '[^']*'),", "`$1, mPhComplaintDesc: 'Sila huraikan masalah anda secara terperinci...', mPhComplaintOrderId: 'cth. ORD123456', mPhComplaintResponse: 'Masukkan respons anda...',"
$lines[4080] = $new
Write-Host "MS updated: $new"

# TA: line 4168
$old = $lines[4167]
$new = $old -replace "(mPhCardName: '[^']*'),", "`$1, mPhComplaintDesc: 'தயவுசெய்து உங்கள் சிக்கலை விரிவாக விவரிக்கவும்...', mPhComplaintOrderId: 'எ.கா. ORD123456', mPhComplaintResponse: 'உங்கள் பதிலை உள்ளிடவும்...',"
$lines[4167] = $new
Write-Host "TA updated: $new"

$lines | Set-Content $file -Encoding UTF8
Write-Host "`nDone! All 4 languages updated."
