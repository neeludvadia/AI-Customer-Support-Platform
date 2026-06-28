"use client";

import React from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/services/auth.service";

interface LogoutButtonProps {
    collapsed?: boolean;
}

export function LogoutButton({ collapsed = false }: LogoutButtonProps) {
    const router = useRouter();

    const handleLogout = async () => {
        await authService.logout();
        router.push("/login");
    };

    return (
        <button 
            onClick={handleLogout}
            className={`flex items-center justify-center rounded-lg bg-gray-50 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-100 hover:text-red-600 ${collapsed ? 'p-2 w-full' : 'px-4 py-2 w-full'}`}
            title={collapsed ? "Logout" : undefined}
        >
            <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            {!collapsed && <span className="ml-2">Logout</span>}
        </button>
    );
}
