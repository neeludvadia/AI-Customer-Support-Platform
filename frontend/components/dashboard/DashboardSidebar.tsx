"use client";

import React, { useEffect, useState } from 'react';
import { systemService } from '@/services/system.service';

export function DashboardSidebar() {
    const [apiStatus, setApiStatus] = useState<'Operational' | 'Down' | 'Loading'>('Loading');

    useEffect(() => {
        const fetchHealth = async () => {
            try {
                await systemService.getHealth();
                setApiStatus('Operational');
            } catch (err) {
                setApiStatus('Down');
            }
        };

        fetchHealth();
        // Optional: poll every 30 seconds
        const interval = setInterval(fetchHealth, 30000);
        return () => clearInterval(interval);
    }, []);

    const StatusIndicator = ({ status, label }: { status: 'Operational' | 'Down' | 'Loading', label: string }) => (
        <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${
                    status === 'Operational' ? 'bg-emerald-500' :
                    status === 'Down' ? 'bg-red-500' : 'bg-yellow-500 animate-pulse'
                }`}></div>
                <span className="text-sm font-medium text-gray-700">{label}</span>
            </div>
            <span className={`text-sm font-medium ${
                status === 'Operational' ? 'text-emerald-600' :
                status === 'Down' ? 'text-red-600' : 'text-yellow-600'
            }`}>
                {status}
            </span>
        </div>
    );

    return (
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
            <h2 className="text-lg font-semibold mb-4 border-b border-gray-200 pb-2">Quick Actions</h2>
            <div className="space-y-3">
                <button className="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
                    Create New Ticket
                </button>
                <button className="w-full flex items-center justify-center px-4 py-2 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
                    Add Knowledge Base Article
                </button>
                <button className="w-full flex items-center justify-center px-4 py-2 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
                    Manage Users
                </button>
            </div>

            <h2 className="text-lg font-semibold mt-8 mb-4 border-b border-gray-200 pb-2">System Status</h2>
            <div className="space-y-4">
                <StatusIndicator status={apiStatus} label="API Service" />
                <StatusIndicator status="Operational" label="Database (Simulated)" />
                <StatusIndicator status="Operational" label="Vector Store (Simulated)" />
            </div>
        </div>
    );
}
