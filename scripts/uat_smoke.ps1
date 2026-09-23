param(
  [string]$ApiBase = "http://localhost:8000",
  [string]$WebBase = "http://localhost:3000",
  [string]$InstitutionCode = "GAINT",
  [string]$AdminEmail = $env:GAINT_UAT_ADMIN_EMAIL,
  [string]$AdminPassword = $env:GAINT_UAT_ADMIN_PASSWORD
)

$ErrorActionPreference = "Stop"

function Assert-Status([string]$Name, [string]$Uri, [int]$Expected = 200) {
  try {
    $r = Invoke-WebRequest -Uri $Uri -UseBasicParsing -TimeoutSec 15
    if ($r.StatusCode -ne $Expected) { throw "$Name returned HTTP $($r.StatusCode), expected $Expected" }
    Write-Host "[PASS] $Name"
  } catch {
    Write-Host "[FAIL] $Name - $($_.Exception.Message)"
    throw
  }
}

Write-Host "GAINT Academy v1.1 local UAT smoke"
Assert-Status "API live" "$ApiBase/health/live"
Assert-Status "API ready" "$ApiBase/health/ready"
Assert-Status "Web login page" "$WebBase/login"

$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$badBody = @{institution_code=$InstitutionCode;email="uat-invalid@example.invalid";password="invalid-password"} | ConvertTo-Json
try {
  Invoke-WebRequest -Uri "$ApiBase/api/v1/auth/login" -Method POST -ContentType "application/json" -Body $badBody -WebSession $session -UseBasicParsing | Out-Null
  throw "Invalid login unexpectedly succeeded"
} catch {
  if ($_.Exception.Response.StatusCode.value__ -ne 401) { throw }
  Write-Host "[PASS] Invalid login rejected"
}

if ($AdminEmail -and $AdminPassword) {
  $loginBody = @{institution_code=$InstitutionCode;email=$AdminEmail;password=$AdminPassword} | ConvertTo-Json
  $login = Invoke-RestMethod -Uri "$ApiBase/api/v1/auth/login" -Method POST -ContentType "application/json" -Body $loginBody -WebSession $session
  if (-not $login.data.user_id) { throw "Admin login response missing user_id" }
  Write-Host "[PASS] Admin login"

  $me = Invoke-RestMethod -Uri "$ApiBase/api/v1/auth/me" -Method GET -WebSession $session
  if (-not $me.data.permissions) { throw "Authenticated /auth/me returned no permissions" }
  Write-Host "[PASS] Authenticated session + RBAC"

  $csrf = Invoke-RestMethod -Uri "$ApiBase/api/v1/auth/csrf" -Method GET -WebSession $session
  if (-not $csrf.data.csrf_token) { throw "CSRF bootstrap returned no token" }
  Write-Host "[PASS] CSRF bootstrap"

  Invoke-RestMethod -Uri "$ApiBase/api/v1/auth/logout" -Method POST -Headers @{"X-CSRF-Token"=$csrf.data.csrf_token} -WebSession $session | Out-Null
  Write-Host "[PASS] Logout"
} else {
  Write-Host "[SKIP] Authenticated smoke: set GAINT_UAT_ADMIN_EMAIL and GAINT_UAT_ADMIN_PASSWORD in the current PowerShell session."
}

Write-Host "Smoke checks completed."
