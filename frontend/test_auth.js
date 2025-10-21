// Test authentication flow
const API_BASE_URL = 'http://localhost:8000';

async function testRegistration() {
    const testUser = {
        username: 'testuser',
        email: 'test@apex.com',
        password: 'testpassword123',
        full_name: 'Test User'
    };

    try {
        const response = await fetch(`${API_BASE_URL}/api/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(testUser)
        });

        const data = await response.json();
        console.log('Registration response:', data);
        
        if (response.ok) {
            console.log('✅ User registered successfully!');
            return true;
        } else {
            console.log('❌ Registration failed:', data.detail);
            return false;
        }
    } catch (error) {
        console.log('❌ Registration error:', error.message);
        return false;
    }
}

async function testLogin() {
    const loginData = {
        username: 'testuser',
        password: 'testpassword123'
    };

    try {
        const response = await fetch(`${API_BASE_URL}/api/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData)
        });

        const data = await response.json();
        console.log('Login response:', data);
        
        if (response.ok) {
            console.log('✅ Login successful!');
            console.log('JWT Token:', data.access_token);
            return data.access_token;
        } else {
            console.log('❌ Login failed:', data.detail);
            return null;
        }
    } catch (error) {
        console.log('❌ Login error:', error.message);
        return null;
    }
}

async function testUserProfile(token) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/user/profile`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });

        const data = await response.json();
        console.log('Profile response:', data);
        
        if (response.ok) {
            console.log('✅ Profile retrieved successfully!');
            console.log('User data:', {
                username: data.username,
                email: data.email,
                full_name: data.full_name,
                created_at: data.created_at
            });
            return true;
        } else {
            console.log('❌ Profile retrieval failed:', data.detail);
            return false;
        }
    } catch (error) {
        console.log('❌ Profile error:', error.message);
        return false;
    }
}

async function runAuthTests() {
    console.log('🚀 Starting APEX Authentication Tests...\n');
    
    // Test registration
    console.log('1️⃣ Testing User Registration...');
    const registrationSuccess = await testRegistration();
    console.log('');
    
    if (registrationSuccess) {
        // Test login
        console.log('2️⃣ Testing User Login...');
        const token = await testLogin();
        console.log('');
        
        if (token) {
            // Test profile retrieval
            console.log('3️⃣ Testing Profile Retrieval...');
            await testUserProfile(token);
            console.log('');
        }
    }
    
    console.log('🏁 Authentication tests completed!');
}

// Run tests if this is executed directly
if (typeof window === 'undefined') {
    runAuthTests();
}