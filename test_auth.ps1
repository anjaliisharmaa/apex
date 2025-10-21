# PowerShell script to test APEX authentication
$API_BASE = "http://localhost:8000"

Write-Host "🚀 Testing APEX Authentication System..." -ForegroundColor Green
Write-Host ""

# Test 1: Register a new user
Write-Host "1️⃣ Testing User Registration..." -ForegroundColor Yellow
$registerData = @{
    username = "testuser"
    email = "test@apex.com"
    password = "testpassword123"
    full_name = "Test User"
} | ConvertTo-Json

try {
    $registerResponse = Invoke-RestMethod -Uri "$API_BASE/api/register" -Method POST -Body $registerData -ContentType "application/json"
    Write-Host "✅ Registration successful!" -ForegroundColor Green
    Write-Host "User ID: $($registerResponse.id)" -ForegroundColor Cyan
    Write-Host "Username: $($registerResponse.username)" -ForegroundColor Cyan
    Write-Host "Email: $($registerResponse.email)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Registration failed: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $errorDetails = $_.Exception.Response.StatusCode
        Write-Host "Status Code: $errorDetails" -ForegroundColor Red
    }
}

Write-Host ""

# Test 2: Login with the user
Write-Host "2️⃣ Testing User Login..." -ForegroundColor Yellow
$loginData = @{
    username = "testuser"
    password = "testpassword123"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "$API_BASE/api/login" -Method POST -Body $loginData -ContentType "application/json"
    Write-Host "✅ Login successful!" -ForegroundColor Green
    Write-Host "Access Token: $($loginResponse.access_token.Substring(0,20))..." -ForegroundColor Cyan
    Write-Host "Token Type: $($loginResponse.token_type)" -ForegroundColor Cyan
    
    $token = $loginResponse.access_token
    
    # Test 3: Get user profile
    Write-Host ""
    Write-Host "3️⃣ Testing User Profile Retrieval..." -ForegroundColor Yellow
    
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }
    
    try {
        $profileResponse = Invoke-RestMethod -Uri "$API_BASE/api/user/profile" -Method GET -Headers $headers
        Write-Host "✅ Profile retrieved successfully!" -ForegroundColor Green
        Write-Host "Username: $($profileResponse.username)" -ForegroundColor Cyan
        Write-Host "Email: $($profileResponse.email)" -ForegroundColor Cyan
        Write-Host "Full Name: $($profileResponse.full_name)" -ForegroundColor Cyan
        Write-Host "Created At: $($profileResponse.created_at)" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Profile retrieval failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ Login failed: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $errorDetails = $_.Exception.Response.StatusCode
        Write-Host "Status Code: $errorDetails" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🏁 Authentication tests completed!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Next steps:" -ForegroundColor Blue
Write-Host "   1. Go to http://localhost:3000/login" -ForegroundColor White
Write-Host "   2. Login with:" -ForegroundColor White
Write-Host "      Email: test@apex.com" -ForegroundColor White
Write-Host "      Password: testpassword123" -ForegroundColor White
Write-Host "   3. You should be redirected to the dashboard!" -ForegroundColor White