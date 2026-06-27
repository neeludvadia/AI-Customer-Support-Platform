import React from "react";
import { LoginForm } from "@/components/login/LoginForm";

export default function LoginPage() {
    return (
        <div className="flex h-full w-full items-center justify-center bg-gray-50 p-4">
            <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-xl ring-1 ring-gray-100">
                <div className="mb-8 text-center">
                    <h1 className="text-3xl font-bold tracking-tight text-gray-900">
                        Welcome Back
                    </h1>
                    <p className="mt-2 text-sm text-gray-500">
                        Sign in to the AI Support Platform
                    </p>
                </div>

                <LoginForm />

                <p className="mt-8 text-center text-sm text-gray-500">
                    Need an account?{" "}
                    <a href="#" className="font-semibold text-indigo-600 hover:text-indigo-500 transition-colors">
                        Contact your admin
                    </a>
                </p>
            </div>
        </div>
    );
}