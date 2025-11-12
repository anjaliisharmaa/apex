'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { apiClient, type CaseData, type AdminStats } from '@/lib/api';
import {
  UserGroupIcon,
  DocumentTextIcon,
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon,
  EyeIcon,
  PlusCircleIcon,
  MinusCircleIcon,
} from '@heroicons/react/24/outline';

interface DashboardStats {
  total_pending: number;
  total_approved: number;
  total_rejected: number;
  new_today: number;
  total_cases: number;
}

export default function AdminDashboard() {
  const [cases, setCases] = useState<CaseData[]>([]);
  const [stats, setStats] = useState<DashboardStats>({
    total_pending: 0,
    total_approved: 0,
    total_rejected: 0,
    new_today: 0,
    total_cases: 0,
  });
  const [isLoading, setIsLoading] = useState(true);
  const [selectedCase, setSelectedCase] = useState<CaseData | null>(null);
  const [filter, setFilter] = useState<'all' | 'pending' | 'approved' | 'rejected'>('all');
  const router = useRouter();

  // Load data from API
  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);

        // Check if user is authenticated
        if (!apiClient.isAuthenticated()) {
          router.push('/login');
          return;
        }

        // Load stats and cases in parallel
        const [statsResult, casesResult] = await Promise.all([
          apiClient.getAdminStats(),
          apiClient.getAdminCases('all', 100, 0)
        ]);

        // Set cases
        setCases(casesResult.cases);

        // Calculate stats from API data
        setStats({
          total_pending: casesResult.cases.filter(c => c.status === 'pending').length,
          total_approved: casesResult.cases.filter(c => c.status === 'approved').length,
          total_rejected: casesResult.cases.filter(c => c.status === 'rejected').length,
          new_today: casesResult.cases.filter(c => {
            const today = new Date().toISOString().split('T')[0];
            return c.submitted_date === today;
          }).length,
          total_cases: casesResult.cases.length,
        });

      } catch (error) {
        console.error('Failed to load admin data:', error);
        // If authentication fails, redirect to login
        if (error instanceof Error && error.message.includes('401')) {
          router.push('/login');
        }
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [router]);

  const getStatusBadge = (status: string) => {
    const variants = {
      pending: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      approved: 'bg-green-100 text-green-800 border-green-200',
      rejected: 'bg-red-100 text-red-800 border-red-200',
      under_review: 'bg-blue-100 text-blue-800 border-blue-200',
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

  const handleStatusChange = async (caseId: string, newStatus: string) => {
    try {
      // Update case status via API
      await apiClient.updateCaseStatus(caseId, {
        status: newStatus,
        notes: `Status updated by admin to ${newStatus}`
      });

      // Update local state
      setCases(prevCases => 
        prevCases.map(case_ => 
          case_.id === caseId 
            ? { ...case_, status: newStatus as any }
            : case_
        )
      );

      // Update stats
      const updatedCases = cases.map(case_ => 
        case_.id === caseId 
          ? { ...case_, status: newStatus as any }
          : case_
      );

      setStats({
        total_pending: updatedCases.filter(c => c.status === 'pending').length,
        total_approved: updatedCases.filter(c => c.status === 'approved').length,
        total_rejected: updatedCases.filter(c => c.status === 'rejected').length,
        new_today: updatedCases.filter(c => {
          const today = new Date().toISOString().split('T')[0];
          return c.submitted_date === today;
        }).length,
        total_cases: updatedCases.length,
      });

    } catch (error) {
      console.error('Failed to update case status:', error);
      alert('Failed to update case status. Please try again.');
    }
  };

  const filteredCases = filter === 'all' 
    ? cases 
    : cases.filter(case_ => case_.status === filter);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
              <p className="text-sm text-gray-600">HR Portal - Manage all employee cases</p>
            </div>
            <div className="flex items-center space-x-4">
              <Button
                variant="outline"
                onClick={() => router.push('/dashboard')}
              >
                Back to User Dashboard
              </Button>
              <Button
                variant="outline"
                onClick={() => router.push('/login')}
              >
                Logout
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-r from-blue-500 to-blue-600 text-white">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Cases</CardTitle>
              <DocumentTextIcon className="h-4 w-4" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.total_cases}</div>
              <p className="text-xs text-blue-100">All submitted cases</p>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-yellow-500 to-yellow-600 text-white">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Pending Cases</CardTitle>
              <ClockIcon className="h-4 w-4" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.total_pending}</div>
              <p className="text-xs text-yellow-100">Awaiting review</p>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-green-500 to-green-600 text-white">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Approved Cases</CardTitle>
              <CheckCircleIcon className="h-4 w-4" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.total_approved}</div>
              <p className="text-xs text-green-100">Successfully approved</p>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-purple-500 to-purple-600 text-white">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">New Today</CardTitle>
              <PlusCircleIcon className="h-4 w-4" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.new_today}</div>
              <p className="text-xs text-purple-100">Submitted today</p>
            </CardContent>
          </Card>
        </div>

        {/* Filters */}
        <div className="mb-6">
          <div className="flex space-x-2">
            {(['all', 'pending', 'approved', 'rejected'] as const).map((status) => (
              <Button
                key={status}
                variant={filter === status ? 'default' : 'outline'}
                onClick={() => setFilter(status)}
                className="capitalize"
              >
                {status === 'all' ? 'All Cases' : `${status.charAt(0).toUpperCase() + status.slice(1)}`}
              </Button>
            ))}
          </div>
        </div>

        {/* Cases Table */}
        <Card>
          <CardHeader>
            <CardTitle>All Cases Management</CardTitle>
            <CardDescription>
              Review and manage all employee cases from across the organization
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full table-auto">
                <thead>
                  <tr className="border-b bg-gray-50">
                    <th className="text-left p-3 font-semibold">Case ID</th>
                    <th className="text-left p-3 font-semibold">Employee</th>
                    <th className="text-left p-3 font-semibold">Department</th>
                    <th className="text-left p-3 font-semibold">Case Type</th>
                    <th className="text-left p-3 font-semibold">Submitted</th>
                    <th className="text-left p-3 font-semibold">Priority</th>
                    <th className="text-left p-3 font-semibold">Status</th>
                    <th className="text-left p-3 font-semibold">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredCases.map((case_) => (
                    <tr key={case_.id} className="border-b hover:bg-gray-50">
                      <td className="p-3">
                        <div className="font-mono text-sm font-medium text-blue-600">
                          {case_.id}
                        </div>
                      </td>
                      <td className="p-3">
                        <div>
                          <div className="font-medium text-gray-900">{case_.user_name}</div>
                          <div className="text-sm text-gray-500">{case_.user_email}</div>
                        </div>
                      </td>
                      <td className="p-3">
                        <div className="text-sm text-gray-900">{case_.department}</div>
                      </td>
                      <td className="p-3">
                        <div className="text-sm font-medium text-gray-900">{case_.case_type}</div>
                        <div className="text-xs text-gray-500 truncate max-w-xs">{case_.title}</div>
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
                      <td className="p-3">
                        <div className="flex space-x-2">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => setSelectedCase(case_)}
                          >
                            <EyeIcon className="h-3 w-3 mr-1" />
                            Review
                          </Button>
                          {case_.status === 'pending' && (
                            <>
                              <Button
                                size="sm"
                                variant="outline"
                                className="text-green-600 border-green-600 hover:bg-green-50"
                                onClick={() => handleStatusChange(case_.id, 'approved')}
                              >
                                <CheckCircleIcon className="h-3 w-3 mr-1" />
                                Approve
                              </Button>
                              <Button
                                size="sm"
                                variant="outline"
                                className="text-red-600 border-red-600 hover:bg-red-50"
                                onClick={() => handleStatusChange(case_.id, 'rejected')}
                              >
                                <XCircleIcon className="h-3 w-3 mr-1" />
                                Reject
                              </Button>
                            </>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {filteredCases.length === 0 && (
              <div className="text-center py-12">
                <DocumentTextIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No cases found</h3>
                <p className="text-gray-500">No cases match the current filter criteria.</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Case Detail Modal */}
        {selectedCase && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h2 className="text-xl font-bold text-gray-900">Case Details</h2>
                  <p className="text-sm text-gray-600">{selectedCase.id}</p>
                </div>
                <Button
                  variant="outline"
                  onClick={() => setSelectedCase(null)}
                >
                  ×
                </Button>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Employee</label>
                  <p className="text-sm text-gray-900">{selectedCase.user_name}</p>
                  <p className="text-xs text-gray-500">{selectedCase.user_email}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Department</label>
                  <p className="text-sm text-gray-900">{selectedCase.department}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Case Type</label>
                  <p className="text-sm text-gray-900">{selectedCase.case_type}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
                  {getPriorityBadge(selectedCase.priority)}
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Submitted Date</label>
                  <p className="text-sm text-gray-900">{selectedCase.submitted_date}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                  {getStatusBadge(selectedCase.status)}
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-1">Case Title</label>
                <p className="text-sm text-gray-900">{selectedCase.title}</p>
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <p className="text-sm text-gray-900 bg-gray-50 p-3 rounded">{selectedCase.description}</p>
              </div>

              {selectedCase.status === 'pending' && (
                <div className="flex space-x-3">
                  <Button
                    className="flex-1 bg-green-600 hover:bg-green-700"
                    onClick={() => {
                      handleStatusChange(selectedCase.id, 'approved');
                      setSelectedCase(null);
                    }}
                  >
                    <CheckCircleIcon className="h-4 w-4 mr-2" />
                    Approve Case
                  </Button>
                  <Button
                    variant="destructive"
                    className="flex-1"
                    onClick={() => {
                      handleStatusChange(selectedCase.id, 'rejected');
                      setSelectedCase(null);
                    }}
                  >
                    <XCircleIcon className="h-4 w-4 mr-2" />
                    Reject Case
                  </Button>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}