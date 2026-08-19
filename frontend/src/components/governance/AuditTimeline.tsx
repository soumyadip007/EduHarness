"use client";

type AuditItem = { id: string; action: string; by: string; at: string };

export default function AuditTimeline({ events }: { events: AuditItem[] }) {
  return (
    <ul>
      {events.map((e) => (
        <li key={e.id}>
          <strong>{e.action}</strong> by {e.by} at {e.at}
        </li>
      ))}
    </ul>
  );
}
