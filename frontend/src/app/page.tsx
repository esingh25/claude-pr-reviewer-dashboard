import RunsTable from "@/components/RunsTable";
import SeverityChart from "@/components/SeverityChart";
import StatCard from "@/components/StatCard";
import TrendChart from "@/components/TrendChart";
import { fetchRecentRuns, fetchSummary } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const [summary, runs] = await Promise.all([fetchSummary(), fetchRecentRuns(20)]);

  return (
    <main className="mx-auto max-w-5xl px-4 py-10">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Claude PR Reviewer Dashboard</h1>
        <p className="mt-2 max-w-2xl text-sm text-gray-600">
          Live quality metrics from{" "}
          <a
            href="https://github.com/esingh25/claude-pr-reviewer"
            className="font-medium text-indigo-600 hover:underline"
          >
            claude-pr-reviewer
          </a>{" "}
          — an AI-powered GitHub/GitLab/Bitbucket pull request reviewer built with Claude. This
          dashboard ingests metrics from real review runs via a public REST API (write access
          requires an API key; the data shown here is read-only and public).
        </p>
      </header>

      {!summary ? (
        <div className="rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
          Couldn&apos;t reach the backend API. If you just deployed this, check that{" "}
          <code className="rounded bg-amber-100 px-1">API_BASE_URL</code> is set correctly.
        </div>
      ) : (
        <>
          <section className="mb-8 grid grid-cols-2 gap-4 sm:grid-cols-4">
            <StatCard label="Total runs" value={summary.total_runs} />
            <StatCard label="Files reviewed" value={summary.total_files_reviewed} />
            <StatCard label="Comments posted" value={summary.total_comments_posted} />
            <StatCard label="Success rate" value={`${Math.round(summary.success_rate * 100)}%`} />
          </section>

          <section className="mb-8 grid gap-6 sm:grid-cols-2">
            <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
              <h2 className="mb-2 text-sm font-semibold text-gray-700">Severity breakdown</h2>
              <SeverityChart severityTotals={summary.severity_totals} />
            </div>
            <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
              <h2 className="mb-2 text-sm font-semibold text-gray-700">Runs over time</h2>
              <TrendChart runsByDay={summary.runs_by_day} />
            </div>
          </section>
        </>
      )}

      <section className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
        <h2 className="mb-4 text-sm font-semibold text-gray-700">Recent runs</h2>
        <RunsTable runs={runs ?? []} />
      </section>

      <footer className="mt-10 text-center text-xs text-gray-400">
        Portfolio project — backend: FastAPI + Postgres (Neon), frontend: Next.js, deployed on
        Vercel.
      </footer>
    </main>
  );
}
