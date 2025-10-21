# Manual API Test Commands

# 1. Register a user
$registerData = @{
    username = "myuser"
    email = "my@email.com"
    password = "mypassword123"
    full_name = "My Name"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/register" -Method POST -Body $registerData -ContentType "application/json"

# 2. Login
$loginData = @{
    username = "myuser"
    password = "mypassword123"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/login" -Method POST -Body $loginData -ContentType "application/json"
$token = $loginResponse.access_token

# 3. Get profile
$headers = @{ "Authorization" = "Bearer $token" }
Invoke-RestMethod -Uri "http://localhost:8000/api/user/profile" -Method GET -Headers $headers