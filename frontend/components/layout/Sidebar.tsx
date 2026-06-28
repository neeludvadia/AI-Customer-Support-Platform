"use client";

import React, { useState } from "react";
import Link from "next/link";
import { LogoutButton } from "@/components/layout/LogoutButton";

const navItems = [
    { 
      name: "Dashboard", 
      href: "/dashboard",
      icon: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
    },
    { 
      name: "Chat", 
      href: "/chat",
      icon: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
    },
    { 
      name: "Tickets", 
      href: "/tickets",
      icon: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
    },
    { 
      name: "Knowledge Base", 
      href: "/knowledge-base",
      icon: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
    },
    { 
      name: "Settings", 
      href: "/settings",
      icon: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
    },
];

export function Sidebar() {
    const [isCollapsed, setIsCollapsed] = useState(false);

    return (
        <aside className={`flex h-screen flex-col border-r border-gray-200 bg-white transition-all duration-300 ${isCollapsed ? 'w-20' : 'w-64'}`}>
            {/* Logo Area */}
            <div className="flex h-16 items-center justify-between border-b border-gray-200 px-4">
                {!isCollapsed && (
                    <span className="text-xl font-bold tracking-tight text-indigo-600 truncate ml-2">
                        AI Support
                    </span>
                )}
                <button 
                    onClick={() => setIsCollapsed(!isCollapsed)}
                    className={`p-2 rounded-lg text-gray-500 hover:bg-gray-100 transition-colors ${isCollapsed ? 'mx-auto' : ''}`}
                    title={isCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
                >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        {isCollapsed ? (
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                        ) : (
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h7" />
                        )}
                    </svg>
                </button>
            </div>
            
            {/* Navigation Links */}
            <nav className="flex-1 space-y-2 px-3 py-4 overflow-y-auto overflow-x-hidden">
                {navItems.map((item) => (
                    <Link
                        key={item.name}
                        href={item.href}
                        className={`flex items-center rounded-lg py-2 transition-colors hover:bg-indigo-50 hover:text-indigo-600 text-gray-700 font-medium ${isCollapsed ? 'justify-center px-0' : 'px-3'}`}
                        title={isCollapsed ? item.name : undefined}
                    >
                        <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            {item.icon}
                        </svg>
                        {!isCollapsed && (
                            <span className="ml-3 truncate text-sm">
                                {item.name}
                            </span>
                        )}
                    </Link>
                ))}
            </nav>
            
            {/* Bottom Actions */}
            <div className="border-t border-gray-200 p-4 flex justify-center">
                {isCollapsed ? (
                    <div title="Logout" className="w-full">
                        <LogoutButton collapsed={true} />
                    </div>
                ) : (
                    <LogoutButton collapsed={false} />
                )}
            </div>
        </aside>
    );
}
