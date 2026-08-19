"use client";

type Props = {
  role: "student" | "tutor";
  text: string;
  scaffoldLevel?: string;
};

export default function MessageBubble({ role, text, scaffoldLevel }: Props) {
  const isStudent = role === "student";
  return (
    <div
      style={{
        alignSelf: isStudent ? "flex-end" : "flex-start",
        background: isStudent ? "#dbeafe" : "#f3f4f6",
        padding: "10px 12px",
        borderRadius: 10,
        marginBottom: 8,
        maxWidth: "80%",
      }}
    >
      <strong>{isStudent ? "Student" : "Tutor"}</strong>
      <div>{text}</div>
      {!isStudent && scaffoldLevel && scaffoldLevel !== "none" ? (
        <div style={{ marginTop: 6, fontSize: 12, color: "#374151" }}>Scaffold: {scaffoldLevel}</div>
      ) : null}
    </div>
  );
}
