"use client";

import { API_BASE } from "@/lib/api";

type ActionPayload = {
  action: string;
  teacher_id?: string;
  rationale?: string;
  rewrite_text?: string;
};

export default function ActionButtons({
  onAction,
  escalationId,
}: {
  onAction: (payload: ActionPayload) => Promise<void>;
  escalationId: string;
}) {
  const actions = ["approve", "rewrite", "freeze_topic", "patch_rule"];
  const [teacherId, setTeacherId] = useState("teacher1");
  const [ownerId, setOwnerId] = useState("teacher1");
  const [rationale, setRationale] = useState("");
  const [rewriteText, setRewriteText] = useState("");
  const [busy, setBusy] = useState(false);
  const [assignStatus, setAssignStatus] = useState("");

  return (
    <div style={{ display: "grid", gap: 12 }}>
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap", alignItems: "center" }}>
        <label>
          Teacher ID
          <input value={teacherId} onChange={(e) => setTeacherId(e.target.value)} style={{ marginLeft: 8 }} />
        </label>
        <label>
          Assign owner
          <input value={ownerId} onChange={(e) => setOwnerId(e.target.value)} style={{ marginLeft: 8 }} />
        </label>
        <button
          type="button"
          onClick={async () => {
            const res = await fetch(`${API_BASE}/api/teacher/queue/${escalationId}/assign`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ owner_id: ownerId }),
            });
            setAssignStatus(res.ok ? `Assigned to ${ownerId}` : "Assign failed");
          }}
        >
          Assign
        </button>
        {assignStatus ? <span>{assignStatus}</span> : null}
      </div>

      <label style={{ display: "block" }}>
        Rationale (required for rewrite / patch_rule / freeze_topic)
        <textarea
          value={rationale}
          onChange={(e) => setRationale(e.target.value)}
          rows={3}
          style={{ display: "block", width: "100%", marginTop: 4 }}
        />
      </label>

      <label style={{ display: "block" }}>
        Rewrite text (for rewrite action — delivered to student on next turn)
        <textarea
          value={rewriteText}
          onChange={(e) => setRewriteText(e.target.value)}
          rows={4}
          style={{ display: "block", width: "100%", marginTop: 4 }}
        />
      </label>

      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        {actions.map((a) => (
          <button
            key={a}
            type="button"
            disabled={busy}
            onClick={async () => {
              setBusy(true);
              try {
                await onAction({
                  action: a,
                  teacher_id: teacherId,
                  rationale,
                  rewrite_text: a === "rewrite" ? rewriteText : undefined,
                });
              } finally {
                setBusy(false);
              }
            }}
          >
            {a}
          </button>
        ))}
      </div>
    </div>
  );
}
