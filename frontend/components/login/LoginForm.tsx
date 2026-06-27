"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/services/auth.service";

export function LoginForm() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setIsLoading(true);

        try {
            // Use the authService to log in
            await authService.login({ email, password });

            // Redirect to dashboard or home on successful login
            router.push("/dashboard"); 
        } catch (err: any) {
            setError(typeof err === "string" ? err : err.message || "An error occurred");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <form onSubmit={handleLogin} className="space-y-6">
            {error && (
                <div className="rounded-md bg-red-50 p-4">
                    <p className="text-sm font-medium text-red-800">{error}</p>
                </div>
            )}
            <div>
                <label className="block text-sm font-medium text-gray-700" htmlFor="email">
                    Email Address
                </label>
                <div className="mt-1">
                    <input
                        id="email"
                        type="email"
                        required
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="block w-full rounded-lg border border-gray-300 px-4 py-3 text-gray-900 placeholder-gray-400 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 sm:text-sm transition-all"
                        placeholder="agent@company.com"
                    />
                </div>
            </div>

            <div>
                <div className="flex items-center justify-between">
                    <label className="block text-sm font-medium text-gray-700" htmlFor="password">
                        Password
                    </label>
                    <a href="#" className="text-sm font-medium text-indigo-600 hover:text-indigo-500 transition-colors">
                        Forgot password?
                    </a>
                </div>
                <div className="mt-1">
                    <input
                        id="password"
                        type="password"
                        required
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="block w-full rounded-lg border border-gray-300 px-4 py-3 text-gray-900 placeholder-gray-400 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 sm:text-sm transition-all"
                        placeholder="••••••••"
                    />
                </div>
            </div>

            <button
                type="submit"
                disabled={isLoading}
                className="flex w-full justify-center rounded-lg bg-indigo-600 px-4 py-3 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-all disabled:opacity-70 disabled:cursor-not-allowed"
            >
                {isLoading ? "Signing in..." : "Sign in"}
            </button>
        </form>
    );
}
