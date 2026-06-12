import Link from 'next/link';
import { getCandidates } from '@/lib/data';

function ScoreBadge({ score }: { score: number }) {
  // Mock logic based on score
  if (score >= 0.7) {
    return <span className="status-strong">{score.toFixed(3)}</span>;
  } else if (score >= 0.45) {
    return <span className="status-uncertain">{score.toFixed(3)}</span>;
  }
  return <span className="status-false">{score.toFixed(3)}</span>;
}

function LabelBadge({ label, classification }: { label?: string; classification?: string }) {
  const effectiveLabel = classification || label || 'Unknown';
  const isFP = effectiveLabel.toLowerCase().includes('false') || effectiveLabel.toLowerCase().includes('suspect') || effectiveLabel.toLowerCase().includes('noise') || effectiveLabel.toLowerCase().includes('blend') || effectiveLabel.toLowerCase().includes('eclipse');
  if (isFP) {
    return <span className="status-false">{effectiveLabel}</span>;
  }
  if (effectiveLabel.toLowerCase().includes('planet') || effectiveLabel.toLowerCase().includes('candidate') || effectiveLabel.toLowerCase().includes('transit')) {
    return <span className="status-strong">{effectiveLabel}</span>;
  }
  return <span className="status-uncertain">{effectiveLabel}</span>;
}

function EmptyState() {
  return (
    <div className="card p-12 text-center flex flex-col items-center justify-center">
      <div className="text-4xl mb-4">🪐</div>
      <h3 className="text-lg font-bold text-text-primary mb-2">No candidates yet</h3>
      <p className="text-text-secondary mb-6 max-w-md">
        The pipeline hasn't processed any targets yet, or the database is currently empty. Run the pipeline to see candidates.
      </p>
      <button className="px-4 py-2 rounded-lg bg-brand-primary text-white font-medium hover:bg-[#4a1b94] transition-colors">
        Run Pipeline
      </button>
    </div>
  );
}

export default async function CandidatesPage() {
  const candidates = await getCandidates();

  return (
    <div className="space-y-8 py-4">
      <header className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight text-text-primary">Candidate List</h1>
        <p className="text-text-secondary">Kepler targets classified by the ExoAstro pipeline. {candidates.length} targets processed.</p>
      </header>

      {/* Info banner */}
      <div className="flex items-start gap-3 px-4 py-3 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-sm">
        <span className="text-lg mt-0.5 text-amber-600">⚠️</span>
        <div>
          <strong className="font-semibold">Note:</strong> AstroNet scores are currently at untrained baseline (~0.5). Scores will update to real predictions after model training on the Kepler DR24 TCE dataset.
        </div>
      </div>

      {candidates.length === 0 ? (
        <EmptyState />
      ) : (
        <div className="card overflow-hidden">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-border-subtle text-xs font-semibold text-text-secondary uppercase tracking-wider bg-surface-alt/80">
                <th className="px-6 py-4">Target</th>
                <th className="px-6 py-4">Classification</th>
                <th className="px-6 py-4">Confidence</th>
                <th className="px-6 py-4 text-right">Period (d)</th>
                <th className="px-6 py-4 text-right">SNR</th>
                <th className="px-6 py-4 text-right">k (Rp/Rs)</th>
                <th className="px-6 py-4 text-center">Odd/Even</th>
                <th className="px-6 py-4"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle">
              {candidates.map((c) => (
                <tr key={c.id} className="table-row-alt hover:bg-brand-primary/5 transition-colors duration-150 group">
                  <td className="px-6 py-4">
                    <div className="font-semibold text-text-primary">{c.targetName}</div>
                    <div className="text-xs text-text-secondary mt-0.5">{c.status}</div>
                  </td>
                  <td className="px-6 py-4"><LabelBadge label={c.label} classification={c.classification} /></td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-16 h-1.5 bg-border-subtle rounded-full overflow-hidden">
                        <div className="h-full bg-brand-primary rounded-full" style={{ width: `${(c.confidence ?? c.astronet_score ?? 0) * 100}%` }} />
                      </div>
                      <ScoreBadge score={c.confidence ?? c.astronet_score ?? 0} />
                    </div>
                  </td>
                  <td className="px-6 py-4 font-mono text-sm text-text-secondary text-right">{c.bls_period.toFixed(3)}</td>
                  <td className="px-6 py-4 font-mono text-sm text-right">
                    <span className={c.snr >= 7.1 ? 'text-emerald-600 font-semibold' : c.snr >= 3 ? 'text-amber-600 font-semibold' : 'text-rose-600 font-semibold'}>
                      {c.snr.toFixed(1)}
                    </span>
                  </td>
                  <td className="px-6 py-4 font-mono text-sm text-text-secondary text-right">{c.fitted_k.toFixed(4)}</td>
                  <td className="px-6 py-4 text-center">
                    <span className={c.odd_even_suspicious ? 'text-rose-600 text-sm font-medium' : 'text-emerald-600 text-sm font-medium'}>
                      {c.odd_even_suspicious ? '⚠️ Suspicious' : '✅ OK'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Link
                      href={`/candidates/${c.id}`}
                      className="text-xs text-brand-secondary font-medium hover:underline opacity-0 group-hover:opacity-100 transition-all duration-150"
                    >
                      Details →
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
