import Link from 'next/link';
import { CandidateSummary } from '@/lib/types';
import fs from 'fs';
import path from 'path';

export default async function CandidatesPage() {
  const dataPath = path.join(process.cwd(), 'public/data/candidates.json');
  let candidates: CandidateSummary[] = [];
  try {
    const fileContents = fs.readFileSync(dataPath, 'utf8');
    candidates = JSON.parse(fileContents);
  } catch (err) {
    console.error(err);
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <header>
        <h1 className="text-3xl font-bold">Candidates</h1>
        <p className="text-slate-400 mt-2">Browse classified targets and vetting results.</p>
      </header>

      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-800/50 border-b border-slate-800 text-sm font-medium text-slate-400">
              <th className="p-4">Target ID</th>
              <th className="p-4">Label</th>
              <th className="p-4">Confidence</th>
              <th className="p-4">Summary</th>
              <th className="p-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 text-sm">
            {candidates.map((c) => (
              <tr key={c.id} className="hover:bg-slate-800/20 transition group">
                <td className="p-4 font-medium text-indigo-300">{c.targetName}</td>
                <td className="p-4">
                  <span className={`px-2 py-1 rounded text-xs ${c.label === 'Confirmed Planet' ? 'bg-emerald-900/30 text-emerald-400 border border-emerald-800' : 'bg-rose-900/30 text-rose-400 border border-rose-800'}`}>
                    {c.label}
                  </span>
                </td>
                <td className="p-4">{(c.confidence * 100).toFixed(1)}%</td>
                <td className="p-4 text-slate-400 truncate max-w-xs">{c.shortSummary}</td>
                <td className="p-4 text-right">
                  <Link href={`/candidates/${c.id}`} className="text-indigo-400 hover:text-indigo-300 font-medium opacity-0 group-hover:opacity-100 transition">
                    View Details &rarr;
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
