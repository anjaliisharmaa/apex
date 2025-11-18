'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ShieldExclamationIcon, EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';
import { apiClient } from '@/lib/api';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [otpCode, setOtpCode] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showOtpStep, setShowOtpStep] = useState(false);
  const [otpSent, setOtpSent] = useState(false);
  const [errors, setErrors] = useState<{[key: string]: string}>({});
  
  const router = useRouter();

  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleGetOTP = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});
    
    // Basic validation
    const newErrors: {[key: string]: string} = {};
    if (!email) newErrors.email = 'Email is required';
    else if (!validateEmail(email)) newErrors.email = 'Please enter a valid email';
    if (!password) newErrors.password = 'Password is required';
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsLoading(true);
    
    try {
      const response = await apiClient.requestOTP({
        email: email,
        password: password
      });
      
      if (response.otp_sent) {
        setShowOtpStep(true);
        setOtpSent(true);
        setErrors({});
      }
    } catch (error: any) {
      console.error('OTP request failed:', error);
      setErrors({ 
        general: error.message.includes('401') 
          ? 'Invalid email or password' 
          : 'Failed to send OTP. Please try again.' 
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleVerifyOTP = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});
    
    if (!otpCode) {
      setErrors({ otp: 'Please enter the OTP code' });
      return;
    }

    if (otpCode.length !== 6) {
      setErrors({ otp: 'OTP must be 6 digits' });
      return;
    }

    setIsLoading(true);
    
    try {
      await apiClient.verifyOTP({
        email: email,
        otp_code: otpCode
      });
      
      console.log('Login successful, redirecting to dashboard...');
      router.push('/dashboard');
    } catch (error: any) {
      console.error('OTP verification failed:', error);
      setErrors({ 
        otp: error.message.includes('401') 
          ? 'Invalid or expired OTP code' 
          : 'OTP verification failed. Please try again.' 
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleBackToCredentials = () => {
    setShowOtpStep(false);
    setOtpSent(false);
    setOtpCode('');
    setErrors({});
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-teal-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <div className="flex justify-center">
            <div className="bg-primary-600 p-3 rounded-full">
              <ShieldExclamationIcon className="h-8 w-8 text-white" />
            </div>
          </div>
          <h2 className="mt-6 text-3xl font-bold text-gray-900">
            Sign in to APEX
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Access your secure legal assistant platform
          </p>
        </div>

        <Card className="shadow-xl border-0">
          <CardHeader className="space-y-1 pb-4">
            <CardTitle className="text-xl font-medium text-center">
              {!showOtpStep ? 'Welcome back' : 'Enter OTP'}
            </CardTitle>
            <CardDescription className="text-center text-gray-500">
              {!showOtpStep 
                ? 'Enter your credentials to get an OTP' 
                : 'Enter the verification code sent to your email'
              }
            </CardDescription>
          </CardHeader>
          <CardContent>
            {errors.general && (
              <div className="mb-4 p-3 rounded-md bg-red-50 border border-red-200">
                <p className="text-sm text-red-600">{errors.general}</p>
              </div>
            )}

            {!showOtpStep ? (
              // Step 1: Email and Password
              <form onSubmit={handleGetOTP} className="space-y-4">
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                    Email Address
                  </label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="your.email@company.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className={`w-full ${errors.email ? 'border-red-500 focus:border-red-500' : ''}`}
                    disabled={isLoading}
                  />
                  {errors.email && (
                    <p className="mt-1 text-sm text-red-600">{errors.email}</p>
                  )}
                </div>

                <div>
                  <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                    Password
                  </label>
                  <div className="relative">
                    <Input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="Enter your password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className={`w-full pr-10 ${errors.password ? 'border-red-500 focus:border-red-500' : ''}`}
                      disabled={isLoading}
                    />
                    <button
                      type="button"
                      className="absolute inset-y-0 right-0 pr-3 flex items-center"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      {showPassword ? (
                        <EyeSlashIcon className="h-4 w-4 text-gray-400" />
                      ) : (
                        <EyeIcon className="h-4 w-4 text-gray-400" />
                      )}
                    </button>
                  </div>
                  {errors.password && (
                    <p className="mt-1 text-sm text-red-600">{errors.password}</p>
                  )}
                </div>

                <Button
                  type="submit"
                  className="w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-md transition duration-200"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Sending OTP...
                    </div>
                  ) : (
                    'Get OTP'
                  )}
                </Button>
              </form>
            ) : (
              // Step 2: OTP Verification
              <div className="space-y-4">
                <div className="text-center mb-6">
                  <div className="bg-green-50 border border-green-200 rounded-md p-3 mb-4">
                    <p className="text-sm text-green-700">
                      📧 OTP request sent for <strong>{email}</strong>
                    </p>
                    
                  </div>
                </div>

                <form onSubmit={handleVerifyOTP} className="space-y-4">
                  <div>
                    <label htmlFor="otpCode" className="block text-sm font-medium text-gray-700 mb-1">
                      Enter OTP Code
                    </label>
                    <Input
                      id="otpCode"
                      type="text"
                      placeholder="000000"
                      value={otpCode}
                      onChange={(e) => setOtpCode(e.target.value)}
                      className={`w-full text-center text-lg tracking-widest ${errors.otp ? 'border-red-500 focus:border-red-500' : ''}`}
                      disabled={isLoading}
                      maxLength={6}
                      pattern="[0-9]{6}"
                    />
                    {errors.otp && (
                      <p className="mt-1 text-sm text-red-600">{errors.otp}</p>
                    )}
                  </div>

                  <Button
                    type="submit"
                    className="w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-md transition duration-200"
                    disabled={isLoading || otpCode.length !== 6}
                  >
                    {isLoading ? (
                      <div className="flex items-center justify-center">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Verifying...
                      </div>
                    ) : (
                      'Sign in'
                    )}
                  </Button>

                  <button
                    type="button"
                    onClick={handleBackToCredentials}
                    className="w-full text-sm text-primary-600 hover:text-primary-500 mt-2"
                    disabled={isLoading}
                  >
                    ← Back to email and password
                  </button>
                </form>
              </div>
            )}

            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600">
                Don't have an account?{' '}
                <a href="/register" className="font-medium text-primary-600 hover:text-primary-500">
                  Sign up here
                </a>
              </p>
            </div>
          </CardContent>
        </Card>

        <div className="text-center">
          <p className="text-xs text-gray-500">
            Protected by enterprise-grade security and encryption
          </p>
        </div>
      </div>
    </div>
  )
}
