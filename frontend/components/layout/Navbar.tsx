import React from "react";

export function Navbar() {
    return (
        <header className="flex h-16 w-full items-center justify-between border-b border-gray-200 bg-white px-6">
            <div className="flex items-center gap-4">
                <h1 className="text-lg font-semibold text-gray-800">Overview</h1>
            </div>
            
            <div className="flex items-center gap-4">
                {/* Simple user profile circle placeholder */}
                <div className="flex h-9 w-9 cursor-pointer items-center justify-center rounded-full bg-indigo-100 text-sm font-bold text-indigo-600 transition-colors hover:bg-indigo-200">
                    JD
                </div>
            </div>
        </header>
    );
}
