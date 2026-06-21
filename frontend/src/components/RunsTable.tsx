import type { ReviewRun } from "@/lib/api";

function StatusBadge({ status }: { status: string }) {
  const isSuccess = status === "success";
  return (
    <span
      className={`rounded-full px-2 py-0.5 text-xs font-medium ${
        isSuccess ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
      }`}
    >
      {status}
    </span>
  );
}

export default function RunsTable({ runs }: { runs: ReviewRun[] }) {
  if (runs.length === 0) {
    return (
      <p className="py-8 text-center text-sm text-gray-500">
        No review runs yet — run the CLI/Action against a real PR to populate this table.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="border-b border-gray-200 text-gray-500">
            <th className="py-2 pr-4 font-medium">Repo</th>
            <th className="py-2 pr-4 font-medium">PR</th>
            <th className="py-2 pr-4 font-medium">Provider</th>
            <th className="py-2 pr-4 font-medium">Files</th>
            <th className="py-2 pr-4 font-medium">Comments</th>
            <th className="py-2 pr-4 font-medium">Duration</th>
            <th className="py-2 pr-4 font-medium">Status</th>
            <th className="py-2 font-medium">When</th>
          </tr>
        </thead>
        <tbody>
          {runs.map((run) => (
            <tr key={run.id} className="border-b border-gray-100">
              <td className="py-2 pr-4 font-mono text-xs">{run.repo}</td>
              <td className="py-2 pr-4">#{run.pr_number}</td>
              <td className="py-2 pr-4 capitalize">{run.provider}</td>
              <td className="py-2 pr-4">{run.files_reviewed}</td>
              <td className="py-2 pr-4">{run.comments_posted}</td>
              <td className="py-2 pr-4">{run.duration_seconds.toFixed(1)}s</td>
              <td className="py-2 pr-4">
                <StatusBadge status={run.status} />
              </td>
              <td className="py-2 text-gray-500">
                {new Date(run.run_timestamp).toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
