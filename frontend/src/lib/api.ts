const API_BASE_URL = process.env.API_BASE_URL ?? "http://localhost:8000";

export type SeverityCounts = {
  critical: number;
  high: number;
  medium: number;
  low: number;
};

export type ReviewRun = {
  id: number;
  repo: string;
  pr_number: number;
  head_sha: string;
  provider: string;
  model: string;
  files_reviewed: number;
  comments_posted: number;
  severity_critical: number;
  severity_high: number;
  severity_medium: number;
  severity_low: number;
  duration_seconds: number;
  status: string;
  run_timestamp: string;
  created_at: string;
};

export type SummaryStats = {
  total_runs: number;
  total_files_reviewed: number;
  total_comments_posted: number;
  success_rate: number;
  severity_totals: SeverityCounts;
  runs_by_provider: Record<string, number>;
  runs_by_day: { date: string; count: number }[];
};

async function fetchJson<T>(path: string): Promise<T | null> {
  try {
    const response = await fetch(`${API_BASE_URL}${path}`, { cache: "no-store" });
    if (!response.ok) return null;
    return (await response.json()) as T;
  } catch {
    return null;
  }
}

export function fetchSummary(): Promise<SummaryStats | null> {
  return fetchJson<SummaryStats>("/api/metrics/summary");
}

export function fetchRecentRuns(limit = 20): Promise<ReviewRun[] | null> {
  return fetchJson<ReviewRun[]>(`/api/metrics?limit=${limit}`);
}
