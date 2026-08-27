<#
  AI Gout Doctor - Tu dong khoi dong
  1. Khoi dong Backend (FastAPI)
  2. Tao Cloudflare Tunnel va lay URL moi
  3. Tu dong cap nhat VITE_API_URL tren Vercel
  4. Redeploy Vercel
#>

$scriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendDir = Join-Path $scriptDir "frontend"
$backendDir  = Join-Path $scriptDir "backend"
$uvicorn     = Join-Path $backendDir "venv\Scripts\uvicorn.exe"
$cfLog       = Join-Path $env:TEMP "ai_gout_cf.log"

Clear-Host
Write-Host ""
Write-Host " ╔══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host " ║   AI GOUT DOCTOR - TU DONG KHOI DONG    ║" -ForegroundColor Cyan
Write-Host " ╚══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Tat cac tien trinh cu (neu co)
Get-Process -Name "uvicorn","cloudflared" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# ─── BUOC 1: Khoi dong Backend ───────────────────────────────────────────────
Write-Host " [1/4] Khoi dong Backend (port 8000)..." -ForegroundColor Yellow

if (-not (Test-Path $uvicorn)) {
    Write-Host "       LOI: Khong tim thay $uvicorn" -ForegroundColor Red
    Read-Host "Nhan Enter de thoat"; exit 1
}

Start-Process -FilePath $uvicorn `
    -ArgumentList "main:app --host 0.0.0.0 --port 8000" `
    -WorkingDirectory $backendDir -WindowStyle Hidden
Start-Sleep -Seconds 5
Write-Host "       Backend dang chay" -ForegroundColor Green

# ─── BUOC 2: Cloudflare Tunnel ───────────────────────────────────────────────
Write-Host " [2/4] Tao Cloudflare Tunnel..." -ForegroundColor Yellow
Write-Host "       Dang cho URL (khoang 10-25 giay)..." -ForegroundColor Gray

Remove-Item $cfLog -Force -ErrorAction SilentlyContinue

$cfProcess = Start-Process cloudflared `
    -ArgumentList "tunnel --url http://localhost:8000 --no-autoupdate" `
    -RedirectStandardError $cfLog -NoNewWindow -PassThru

$tunnelUrl = $null
for ($i = 0; $i -lt 25; $i++) {
    Start-Sleep -Seconds 2
    $content = Get-Content $cfLog -Raw -ErrorAction SilentlyContinue
    if ($content -match 'https://[a-zA-Z0-9-]+\.trycloudflare\.com') {
        $tunnelUrl = $Matches[0]; break
    }
}

if (-not $tunnelUrl) {
    Write-Host " LOI: Khong lay duoc tunnel URL!" -ForegroundColor Red
    Write-Host " Log cloudflared:" -ForegroundColor Gray
    Get-Content $cfLog -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "   $_" }
    Write-Host ""
    Read-Host "Nhan Enter de thoat"; exit 1
}

Write-Host "       Tunnel: $tunnelUrl" -ForegroundColor Green

# ─── BUOC 3: Cap nhat bien moi truong Vercel ─────────────────────────────────
Write-Host " [3/4] Cap nhat VITE_API_URL tren Vercel..." -ForegroundColor Yellow
Push-Location $frontendDir

# Xoa bien cu (bo qua loi neu chua co)
& vercel env rm VITE_API_URL production --yes 2>&1 | Out-Null

# Them bien moi (doc tu stdin)
$psi = [System.Diagnostics.ProcessStartInfo]::new()
$psi.FileName = "vercel"
$psi.Arguments = "env add VITE_API_URL production"
$psi.RedirectStandardInput = $true
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.UseShellExecute = $false
$psi.WorkingDirectory = $frontendDir
$envProc = [System.Diagnostics.Process]::Start($psi)
$envProc.StandardInput.WriteLine($tunnelUrl)
$envProc.StandardInput.Close()
$envProc.WaitForExit()

Write-Host "       VITE_API_URL = $tunnelUrl" -ForegroundColor Green

# ─── BUOC 4: Redeploy Vercel ─────────────────────────────────────────────────
Write-Host " [4/4] Redeploy Vercel (30-60 giay)..." -ForegroundColor Yellow
$output = & vercel --prod --yes 2>&1
$output | ForEach-Object { Write-Host "       $_" -ForegroundColor DarkGray }

# Tim URL production trong output
$appUrl = "https://ai-gout-doctor.vercel.app"
foreach ($line in $output) {
    if ($line -match 'https://[^\s]+\.vercel\.app') {
        $appUrl = $Matches[0]
    }
}

Pop-Location

# ─── HOAN TAT ─────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host " ╔══════════════════════════════════════════╗" -ForegroundColor Green
Write-Host " ║              XONG! App san sang           ║" -ForegroundColor Green
Write-Host " ╚══════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "   App URL : $appUrl" -ForegroundColor White
Write-Host "   Tunnel  : $tunnelUrl" -ForegroundColor White
Write-Host ""
Write-Host "   !! GIU CUA SO NAY MO !!" -ForegroundColor Red
Write-Host "   Dong cua so = tat backend va tunnel" -ForegroundColor Gray
Write-Host ""
Write-Host "   (Nhan Ctrl+C de dung)" -ForegroundColor DarkGray

# Giu cua so mo cho den khi cloudflared dung
try { Wait-Process -Id $cfProcess.Id } catch { }
