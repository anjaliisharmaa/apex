'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { apiClient, type EmployeeDetails } from '@/lib/api';
import {
  ArrowLeftIcon,
  UserIcon,
  PhoneIcon,
  MapPinIcon,
  BriefcaseIcon,
  CalendarIcon,
  ShieldCheckIcon,
  AcademicCapIcon,
  ClockIcon,
} from '@heroicons/react/24/outline';

export default function EmployeeDetailsPage() {
  const [employee, setEmployee] = useState<EmployeeDetails | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const params = useParams();
  
  const employeeEmail = Array.isArray(params.email) ? params.email[0] : params.email;

  useEffect(() => {
    const loadEmployeeDetails = async () => {
      try {
        setIsLoading(true);
        setError(null);

        if (!apiClient.isAuthenticated()) {
          router.push('/login');
          return;
        }

        if (!employeeEmail) {
          setError('No employee email provided');
          return;
        }

        // Decode the email parameter
        const decodedEmail = decodeURIComponent(employeeEmail);
        const employeeData = await apiClient.getEmployeeDetails(decodedEmail);
        setEmployee(employeeData);

      } catch (error) {
        console.error('Failed to load employee details:', error);
        setError('Failed to load employee details');
        
        if (error instanceof Error && error.message.includes('401')) {
          router.push('/login');
        }
      } finally {
        setIsLoading(false);
      }
    };

    loadEmployeeDetails();
  }, [employeeEmail, router]);

  const getStatusBadge = (status: string) => {
    const variants = {
      pending: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      approved: 'bg-green-100 text-green-800 border-green-200',
      rejected: 'bg-red-100 text-red-800 border-red-200',
      under_review: 'bg-blue-100 text-blue-800 border-blue-200',
      resolved: 'bg-gray-100 text-gray-800 border-gray-200',
    };

    return (
      <Badge className={`${variants[status as keyof typeof variants]} border`}>
        {status.charAt(0).toUpperCase() + status.slice(1).replace('_', ' ')}
      </Badge>
    );
  };

  const getPriorityBadge = (priority: string) => {
    const variants = {
      high: 'bg-red-50 text-red-700 border-red-200',
      medium: 'bg-orange-50 text-orange-700 border-orange-200',
      low: 'bg-gray-50 text-gray-700 border-gray-200',
    };

    return (
      <Badge variant="outline" className={variants[priority as keyof typeof variants]}>
        {priority.charAt(0).toUpperCase() + priority.slice(1)}
      </Badge>
    );
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error || !employee) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Error Loading Employee Details</h2>
          <p className="text-gray-600 mb-4">{error || 'Employee not found'}</p>
          <Button onClick={() => router.push('/admin')}>
            <ArrowLeftIcon className="h-4 w-4 mr-2" />
            Back to Admin Dashboard
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <Button
                variant="outline"
                onClick={() => router.push('/admin')}
              >
                <ArrowLeftIcon className="h-4 w-4 mr-2" />
                Back to Admin Dashboard
              </Button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Employee Details</h1>
                <p className="text-sm text-gray-600">{employee.name} - {employee.department}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Employee Information */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <UserIcon className="h-5 w-5 mr-2" />
                  Employee Information
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                  <p className="text-sm text-gray-900 font-medium">{employee.name}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Employee ID</label>
                  <p className="text-sm text-gray-900 font-mono">{employee.employee_id}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <p className="text-sm text-blue-600">{employee.email}</p>
                </div>

                <div className="flex items-center">
                  <PhoneIcon className="h-4 w-4 mr-2 text-gray-500" />
                  <p className="text-sm text-gray-900">{employee.phone}</p>
                </div>

                <div className="flex items-center">
                  <MapPinIcon className="h-4 w-4 mr-2 text-gray-500" />
                  <p className="text-sm text-gray-900">{employee.location}</p>
                </div>

                <div className="flex items-center">
                  <BriefcaseIcon className="h-4 w-4 mr-2 text-gray-500" />
                  <p className="text-sm text-gray-900">{employee.role}</p>
                </div>

                <div className="flex items-center">
                  <CalendarIcon className="h-4 w-4 mr-2 text-gray-500" />
                  <p className="text-sm text-gray-900">Joined: {new Date(employee.join_date).toLocaleDateString()}</p>
                </div>

                <div className="flex items-center">
                  <ShieldCheckIcon className="h-4 w-4 mr-2 text-gray-500" />
                  <p className="text-sm text-gray-900">Clearance: {employee.security_clearance}</p>
                </div>

                <div className="flex items-center">
                  <AcademicCapIcon className="h-4 w-4 mr-2 text-gray-500" />
                  <p className="text-sm text-gray-900">{employee.specialization}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Supervisor</label>
                  <p className="text-sm text-gray-900">{employee.supervisor}</p>
                </div>
              </CardContent>
            </Card>

            {/* Performance Summary */}
            <Card className="mt-6">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <ClockIcon className="h-5 w-5 mr-2" />
                  Performance Summary
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{employee.performance_summary.total_cases}</div>
                    <div className="text-xs text-gray-500">Total Cases</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-yellow-600">{employee.performance_summary.pending_cases}</div>
                    <div className="text-xs text-gray-500">Pending Cases</div>
                  </div>
                </div>
                <div className="mt-4 text-center">
                  <div className="text-sm text-gray-600">
                    Avg. Resolution: <span className="font-medium">{employee.performance_summary.average_resolution_time}</span>
                  </div>
                  <div className="text-sm text-gray-600">
                    Last Case: <span className="font-medium">{new Date(employee.performance_summary.last_case_date).toLocaleDateString()}</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Case History */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>Case History</CardTitle>
                <CardDescription>
                  All cases submitted by {employee.name}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full table-auto">
                    <thead>
                      <tr className="border-b bg-gray-50">
                        <th className="text-left p-3 font-semibold">Case ID</th>
                        <th className="text-left p-3 font-semibold">Type</th>
                        <th className="text-left p-3 font-semibold">Title</th>
                        <th className="text-left p-3 font-semibold">Submitted</th>
                        <th className="text-left p-3 font-semibold">Priority</th>
                        <th className="text-left p-3 font-semibold">Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {employee.cases.map((case_) => (
                        <tr key={case_.id} className="border-b hover:bg-gray-50">
                          <td className="p-3">
                            <div className="font-mono text-sm font-medium text-blue-600">
                              {case_.id}
                            </div>
                          </td>
                          <td className="p-3">
                            <div className="text-sm font-medium text-gray-900">{case_.case_type}</div>
                          </td>
                          <td className="p-3">
                            <div className="text-sm text-gray-900">{case_.title}</div>
                          </td>
                          <td className="p-3">
                            <div className="text-sm text-gray-900">{case_.submitted_date}</div>
                          </td>
                          <td className="p-3">
                            {getPriorityBadge(case_.priority)}
                          </td>
                          <td className="p-3">
                            {getStatusBadge(case_.status)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {employee.cases.length === 0 && (
                  <div className="text-center py-12">
                    <UserIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No cases found</h3>
                    <p className="text-gray-500">This employee has not submitted any cases yet.</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}