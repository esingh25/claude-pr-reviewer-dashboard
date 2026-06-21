"use client";

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import type { SeverityCounts } from "@/lib/api";

const COLORS: Record<keyof SeverityCounts, string> = {
  critical: "#dc2626",
  high: "#f97316",
  medium: "#eab308",
  low: "#22c55e",
};

export default function SeverityChart({ severityTotals }: { severityTotals: SeverityCounts }) {
  const data = (Object.keys(severityTotals) as (keyof SeverityCounts)[]).map((key) => ({
    severity: key,
    count: severityTotals[key],
    fill: COLORS[key],
  }));

  return (
    <ResponsiveContainer width="100%" height={220}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
        <XAxis dataKey="severity" tick={{ fontSize: 12 }} />
        <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
        <Tooltip />
        <Bar dataKey="count" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
