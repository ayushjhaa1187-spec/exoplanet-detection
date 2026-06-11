import Link from 'next/link';
import { getCandidates } from '@/lib/data';
import { Candidate } from '@/lib/types';

function ScoreBadge({ score }: { score: number }) {
  const cls = score >= 0.7 ? 'score-high' : score >= 0.45 ? 'score-mid' : 'score-low';
  return (
    <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold ${cls}`}>
      {score.toFixed(3)}
    </span>
  );
}

function LabelBadge({ label }: { label: string }) {
  const isFP = label.toLowerCase().includes('false') || label.toLowerCase().includes('suspect');
  return (
    <span className={`px-2 py-1 rounded-md text-xs font-semibold ${
      isFP ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
    }`}>
      {label}
    </span>
  );
}

export default async function CandidatesPage() {
  const candidates = await getCandidates();

  return (
    <div className="space-y-8">
      <header className="space-y-1">
        <h1 className="text-3xl font-bold tracking-tight">Candidate List</h1>
        <p className="text-slate-400">Kepler targets classified by the ExoAstro pipeline. {candidates.length} targets processed.</p>
      </header>

      {/* Info banner */}
      <div className="flex items-start gap-3 px-4 py-3 rounded-xl bg-amber-500/5 border border-amber-500/20 text-amber-300 text-sm">
        <span className="text-lg mt-0.5">⚠️</span>
        <div>
          <strong>Note:</strong> AstroNet scores are currently at untrained baseline (~0.5). Scores will update to real predictions after model training on the Kepler DR24 TCE dataset.
        </div>
      </div>

      <div className="glass rounded-2xl overflow-hidden">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-slate-800/60 text-xs font-semibold text-slate-500 uppercase tracking-wider">
              <th className="px-6 py-4">Target</th>
              <th className="px-6 py-4">Classification</th>
              <th className="px-6 py-4">AstroNet Score</th>
              <th className="px-6 py-4">Period (days)</th>
              <th className="px-6 py-4">SNR</th>
              <th className="px-6 py-4">k (Rp/Rs)</th>
              <th className="px-6 py-4">Odd/Even</th>
              <th className="px-6 py-4"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/40">
            {candidates.map((c) => (
              <tr key={c.id} className="hover:bg-slate-800/20 transition-colors duration-150 group">
                <td className="px-6 py-4">
                  <div className="font-semibold text-slate-200">{c.targetName}</div>
                  <div className="text-xs text-slate-600 mt-0.5">{c.status}</div>
                </td>
                <td className="px-6 py-4"><LabelBadge label={c.label} /></td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <div className="w-16 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                      <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${c.astronet_score * 100}%` }} />
                    </div>
                    <ScoreBadge score={c.astronet_score} />
                  </div>
                </td>
                <td className="px-6 py-4 font-mono text-sm text-slate-300">{c.bls_period.toFixed(3)}</td>
                <td className="px-6 py-4 font-mono text-sm">
                  <span className={c.snr >= 7.1 ? 'text-emerald-400' : c.snr >= 3 ? 'text-amber-400' : 'text-rose-400'}>
                    {c.snr.toFixed(1)}
                  </span>
                </td>
                <td className="px-6 py-4 font-mono text-sm text-slate-300">{c.fitted_k.toFixed(4)}</td>
                <td className="px-6 py-4">
                  <span className={c.odd_even_suspicious ? 'text-rose-400 text-sm' : 'text-emerald-400 text-sm'}>
                    {c.odd_even_suspicious ? '⚠️ Suspicious' : '✅ OK'}
                  </span>
                </td>
                <td className="px-6 py-4 text-right">
                  <Link
                    href={`/candidates/${c.id}`}
                    className="text-xs text-indigo-400 hover:text-indigo-300 opacity-0 group-hover:opacity-100 transition-all duration-150 font-medium"
                  >
                    Details →
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
