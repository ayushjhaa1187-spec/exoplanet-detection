import fs from 'fs';
import path from 'path';

export default async function ReportsPage() {
  const reportsDir = path.join(process.cwd(), 'public/reports');
  let reports: string[] = [];
  try {
    reports = fs.readdirSync(reportsDir).filter(f => f.endsWith('.pdf'));
  } catch (err) {
    console.error(err);
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <header>
        <h1 className="text-3xl font-bold">Vetting Reports</h1>
        <p className="text-slate-400 mt-2">Generated PDF summaries for confirmed and flagged candidates.</p>
      </header>

      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-800/50 border-b border-slate-800 text-sm font-medium text-slate-400">
              <th className="p-4">Report Document</th>
              <th className="p-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 text-sm">
            {reports.length === 0 && (
              <tr><td colSpan={2} className="p-4 text-center text-slate-500">No reports generated yet.</td></tr>
            )}
            {reports.map((report) => (
              <tr key={report} className="hover:bg-slate-800/20 transition group">
                <td className="p-4 font-medium text-indigo-300 flex items-center gap-3">
                  <svg className="w-5 h-5 text-rose-400" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd"></path></svg>
                  {report}
                </td>
                <td className="p-4 text-right">
                  <a href={`/reports/${report}`} target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 font-medium">
                    Download PDF &darr;
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
