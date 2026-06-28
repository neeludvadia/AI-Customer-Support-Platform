import React from "react";
import Link from "next/link";
import { RegisterForm } from "@/components/register/RegisterForm";

export default function RegisterPage() {
    return (
        <div className="flex h-full w-full items-center justify-center bg-gray-50 p-4">
            <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-xl ring-1 ring-gray-100">
                <div className="mb-8 text-center">
                    <h1 className="text-3xl font-bold tracking-tight text-gray-900">
                        Create an Account
                    </h1>
                    <p className="mt-2 text-sm text-gray-500">
                        Join the AI Support Platform
                    </p>
                </div>

                <RegisterForm />

                <p className="mt-8 text-center text-sm text-gray-500">
                    Already have an account?{" "}
                    <Link href="/login" className="font-semibold text-indigo-600 hover:text-indigo-500 transition-colors">
                        Sign in
                    </Link>
                </p>
            </div>
        </div>
    );
}
