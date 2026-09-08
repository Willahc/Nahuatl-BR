import type { ReactNode } from "react";

const VARIANT: Record<string, string> = {
  OBSERVED: "pill--observed",
  REPORTED: "pill--reported",
  INFERRED: "pill--inferred",
  RECONSTRUCTED: "pill--reconstructed",
  EDITORIAL: "pill--editorial",
  DRAFT: "pill--draft",
  IN_REVIEW: "pill--inreview",
  PUBLISHED: "pill--published",
  ACCEPT: "pill--accept",
  REJECT: "pill--reject",
  HIGH: "pill--high",
  MEDIUM: "pill--medium",
  LOW: "pill--low",
};

export function Pill({ children, kind }: { children: ReactNode; kind?: string }) {
  return <span className={`pill ${VARIANT[(kind ?? "").toUpperCase()] ?? ""}`}>{children}</span>;
}