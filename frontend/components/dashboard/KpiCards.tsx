"use client";

import React, { useEffect, useState } from 'react';
import { adminService } from '@/services/admin.service';
import { DashboardMetrics } from '@/types/admin';

export function KpiCards() {
    const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const data = await adminService.getMetrics();
                setMetrics(data);
                setError(null);
            } catch (err: any) {
                setError(err.toString());
            } finally {
                setLoading(false);
            }
        };

        fetchMetrics();
    }, []);

    if (loading) {
        return <div className="text-sm text-gray-500 animate-pulse">Loading metrics...</div>;
    }

    if (error) {
        return (
            <div className="bg-red-50 text-red-600 p-4 rounded-xl text-sm border border-red-200">
                Failed to load metrics: {error}. (Ensure you are logged in as an Admin).
            </div>
        );
    }

    if (!metrics) return null;

    const kpis = [
        { title: "Total Tickets", value: metrics.total_tickets.toString(), change: "Lifetime", trend: "up" },
        { title: "Open Tickets", value: metrics.open_tickets.toString(), change: "Requires attention", trend: "down" },
        { title: "Total Messages", value: metrics.total_messages.toString(), change: "Across all chats", trend: "up" },
        { title: "KB Articles", value: metrics.total_documents.toString(), change: "Indexed in RAG", trend: "up" },
    ];

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {kpis.map((kpi, index) => (
                <div key={index} className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col justify-between">
                    <div>
                        <p className="text-sm font-medium text-gray-500">{kpi.title}</p>
                        <h3 className="text-3xl font-bold text-gray-900 mt-2">{kpi.value}</h3>
                    </div>
                    <div className={`mt-4 text-sm font-medium ${kpi.trend === 'up' ? 'text-emerald-600' : 'text-rose-600'}`}>
                        {kpi.change}
                    </div>
                </div>
            ))}
        </div>
    );
}
