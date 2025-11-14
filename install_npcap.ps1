# Npcap yükleyici script
# Bu script yönetici yetkisiyle çalıştırılmalıdır

Write-Host "=== Npcap Yükleme Script ==="
Write-Host ""

# Admin kontrolü
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "HATA: Bu script yönetici yetkisiyle çalıştırılmalıdır!" -ForegroundColor Red
    Write-Host "Lütfen PowerShell'i yönetici olarak açıp şu komutu çalıştırın:" -ForegroundColor Yellow
    Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
    Write-Host ""
    Write-Host "Ardından script'i tekrar çalıştırın:"
    Write-Host "powershell -ExecutionPolicy Bypass -File $PSScriptRoot\install_npcap.ps1"
    exit 1
}

$url = "https://nmap.org/npcap/dist/npcap-latest.exe"
$tempDir = $env:TEMP
$output = Join-Path $tempDir "npcap-latest.exe"

Write-Host "Npcap indiriliyor..."
Write-Host "URL: $url"
Write-Host "Hedef: $output"
Write-Host ""

try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $url -OutFile $output -UseBasicParsing
    Write-Host "✓ İndirme tamamlandı." -ForegroundColor Green
}
catch {
    Write-Host "✗ İndirme başarısız oldu: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Kurulum başlatılıyor..."
Write-Host "Lütfen kurulum penceresinde 'WinPcap API-compatible Mode' seçeneğini işaretleyin."
Write-Host ""

try {
    Start-Process -FilePath $output -Wait
    Write-Host "✓ Kurulum tamamlandı." -ForegroundColor Green
}
catch {
    Write-Host "✗ Kurulum başlatılamadı: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Kurulum Başarılı ==="
Write-Host "Lütfen sistemi yeniden başlatıp web uygulamasını yeniden çalıştırın."
