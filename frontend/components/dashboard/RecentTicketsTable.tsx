"use client";

import React, { useEffect, useState } from 'react';
import { ticketService } from '@/services/ticket.service';
import { TicketResponse } from '@/types/ticket';

export function RecentTicketsTable() {
    const [tickets, setTickets] = useState<TicketResponse[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchTickets = async () => {
            try {
                const data = await ticketService.getTickets();
                // Sort by created_at descending and take top 5
                const sorted = data.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
                setTickets(sorted.slice(0, 5));
                setError(null);
            } catch (err: any) {
                setError(err.toString());
            } finally {
                setLoading(false);
            }
        };

        fetchTickets();
    }, []);

    const formatTimeAgo = (dateString: string) => {
        const date = new Date(dateString);
        const now = new Date();
        const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / 60000);
        
        if (diffInMinutes < 60) return `${diffInMinutes} mins ago`;
        const diffInHours = Math.floor(diffInMinutes / 60);
        if (diffInHours < 24) return `${diffInHours} hrs ago`;
        return `${Math.floor(diffInHours / 24)} days ago`;
    };

    return (
        <div className="lg:col-span-2 bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
            <div className="p-5 border-b border-gray-200 flex justify-between items-center">
                <h2 className="text-lg font-semibold">Recent Tickets</h2>
                <button className="text-sm font-medium text-blue-600 hover:text-blue-800">View All</button>
            </div>
            
            {loading ? (
                <div className="p-5 text-sm text-gray-500 animate-pulse">Loading tickets...</div>
            ) : error ? (
                <div className="p-5 text-sm text-red-600 bg-red-50 border-t border-red-100">Failed to load tickets: {error}</div>
            ) : tickets.length === 0 ? (
                <div className="p-5 text-sm text-gray-500">No tickets found.</div>
            ) : (
                <div className="overflow-x-auto">
                    <table className="w-full text-sm text-left">
                        <thead className="text-xs text-gray-500 uppercase bg-gray-50 border-b border-gray-200">
                            <tr>
                                <th className="px-6 py-3 font-medium">Ticket ID</th>
                                <th className="px-6 py-3 font-medium">Subject</th>
                                <th className="px-6 py-3 font-medium">Status</th>
                                <th className="px-6 py-3 font-medium">Time</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                            {tickets.map((ticket) => (
                                <tr key={ticket.id} className="hover:bg-gray-50 transition-colors">
                                    <td className="px-6 py-4 font-medium text-gray-900">T-{ticket.id}</td>
                                    <td className="px-6 py-4 text-gray-700 max-w-xs truncate" title={ticket.question}>
                                        {ticket.question}
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                                            ticket.status.toLowerCase() === 'open' ? 'bg-amber-100 text-amber-800' :
                                            ticket.status.toLowerCase() === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                                            'bg-emerald-100 text-emerald-800'
                                        }`}>
                                            {ticket.status.replace('_', ' ').toUpperCase()}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 text-gray-500 whitespace-nowrap">
                                        {formatTimeAgo(ticket.created_at)}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
