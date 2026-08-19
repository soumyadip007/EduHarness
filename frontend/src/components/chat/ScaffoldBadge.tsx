"use client";

export default function ScaffoldBadge({ level }: { level: string }) {
  if (!level || level === "none") return null;
  return (
    <span
      style={{
        display: "inline-block",
        marginTop: 6,
        fontSize: 12,
        color: "#1f2937",
        background: "#e5e7eb",
        borderRadius: 999,
        padding: "2px 8px",
      }}
    >
      Scaffold: {level}
    </span>
  );
}
