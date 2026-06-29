import React from 'react';
import { KpiCards } from '@/components/dashboard/KpiCards';
import { RecentTicketsTable } from '@/components/dashboard/RecentTicketsTable';
import { DashboardSidebar } from '@/components/dashboard/DashboardSidebar';

export default function DashboardPage() {
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-2xl font-semibold tracking-tight">Dashboard Overview</h1>
                <div className="text-sm text-gray-500">
                    Last updated: {new Date().toLocaleDateString()}
                </div>
            </div>

            {/* KPI Cards */}
            <KpiCards />

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Recent Tickets Table */}
                <RecentTicketsTable />

                {/* System Activity / Quick Actions */}
                <DashboardSidebar />
            </div>
        </div>
    );
}