import React from "react";
import { TicketList } from "@/components/tickets/TicketList";

export default function TicketsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Support Tickets</h1>
        <p className="mt-2 text-sm text-gray-600">
          View and manage your escalation tickets here.
        </p>
      </div>

      <TicketList />
    </div>
  );
}
