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
    <div className="space-y-8 py-4">
      <header className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight text-text-primary">Vetting Reports</h1>
        <p className="text-text-secondary text-lg mt-2">Generated PDF summaries for confirmed and flagged candidates.</p>
      </header>

      <div className="card overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-surface-alt/80 border-b border-border-subtle text-xs font-semibold text-text-secondary uppercase tracking-wider">
              <th className="px-6 py-4">Report Document</th>
              <th className="px-6 py-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border-subtle text-sm">
            {reports.length === 0 && (
              <tr>
                <td colSpan={2} className="px-6 py-12 text-center text-text-secondary">
                  <div className="text-4xl mb-3 opacity-50">📄</div>
                  No PDF reports generated yet.
                </td>
              </tr>
            )}
            {reports.map((report) => (
              <tr key={report} className="hover:bg-brand-primary/5 transition-colors group">
                <td className="px-6 py-4 font-medium text-text-primary flex items-center gap-3">
                  <div className="w-8 h-8 rounded bg-rose-50 border border-rose-100 flex items-center justify-center">
                    <svg className="w-4 h-4 text-rose-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd"></path>
                    </svg>
                  </div>
                  {report}
                </td>
                <td className="px-6 py-4 text-right">
                  <a href={`/reports/${report}`} target="_blank" rel="noopener noreferrer" className="text-sm font-medium text-brand-secondary hover:text-brand-primary transition-colors flex items-center justify-end gap-1">
                    Download PDF 
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
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
