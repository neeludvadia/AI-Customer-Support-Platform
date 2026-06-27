import React from "react";
import Link from "next/link";

const navItems = [
    { name: "Dashboard", href: "/dashboard" },
    { name: "Tickets", href: "/tickets" },
    { name: "Knowledge Base", href: "/knowledge-base" },
    { name: "Settings", href: "/settings" },
];

export function Sidebar() {
    return (
        <aside className="flex h-screen w-64 flex-col border-r border-gray-200 bg-white">
            {/* Logo Area */}
            <div className="flex h-16 items-center border-b border-gray-200 px-6">
                <span className="text-xl font-bold tracking-tight text-indigo-600">
                    AI Support
                </span>
            </div>
            
            {/* Navigation Links */}
            <nav className="flex-1 space-y-1 px-3 py-4">
                {navItems.map((item) => (
                    <Link
                        key={item.name}
                        href={item.href}
                        className="flex items-center rounded-lg px-3 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-indigo-50 hover:text-indigo-600"
                    >
                        {item.name}
                    </Link>
                ))}
            </nav>
            
            {/* Bottom Actions */}
            <div className="border-t border-gray-200 p-4">
                <button className="flex w-full items-center justify-center rounded-lg bg-gray-50 px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-100 hover:text-red-600">
                    Logout
                </button>
            </div>
        </aside>
    );
}
