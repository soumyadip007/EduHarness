"use client";

export default function ActionButtons({ onAction }: { onAction: (action: string) => void }) {
  const actions = ["approve", "rewrite", "freeze_topic", "patch_rule"];
  return (
    <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
      {actions.map((a) => (
        <button key={a} onClick={() => onAction(a)}>{a}</button>
      ))}
    </div>
  );
}
