import React from "react";
import { KnowledgeBaseList } from "@/components/knowledge-base/KnowledgeBaseList";

export default function KnowledgeBasePage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Knowledge Base</h1>
        <p className="mt-2 text-sm text-gray-600">
          Upload and manage PDF documents for the AI to learn from.
        </p>
      </div>

      <KnowledgeBaseList />
    </div>
  );
}
