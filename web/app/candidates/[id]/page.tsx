import Link from 'next/link';
import { notFound } from 'next/navigation';
import PlotImage from '@/components/PlotImage';
import { getCandidateById } from '@/lib/data';
import { Candidate } from '@/lib/types';

type PageParams = Promise<{ id: string }>;

function VettingCard({ ok, label, detail }: { ok: boolean; label: string; detail: string }) {
  return (
    <div className={`flex items-start gap-3 p-4 rounded-xl border ${
      ok ? 'bg-emerald-500/5 border-emerald-500/20' : 'bg-rose-500/5 border-rose-500/20'
    }`}>
      <span className="text-lg mt-0.5">{ok ? '✅' : '⚠️'}</span>
      <div>
        <div className={`text-sm font-semibold ${ok ? 'text-emerald-300' : 'text-rose-300'}`}>{label}</div>
        <div className="text-xs text-slate-400 mt-0.5">{detail}</div>
      </div>
    </div>
  );
}

function MetricRow({ label, value, mono }: { label: string; value: string; mono?: boolean }) {
  return (
    <div className="flex items-center justify-between py-3 border-b border-slate-800/50 last:border-0">
      <span className="text-sm text-slate-400">{label}</span>
      <span className={`text-sm font-semibold text-slate-100 ${mono ? 'font-mono' : ''}`}>{value}</span>
    </div>
  );
}

export default async function CandidateDetailPage({ params }: { params: PageParams }) {
  const { id } = await params;
  const detail = await getCandidateById(id);
  if (!detail) notFound();

  const isFP = detail.label.toLowerCase().includes('false') || detail.label.toLowerCase().includes('suspect');
  const scoreColor = detail.astronet_score >= 0.7 ? 'text-emerald-400' : detail.astronet_score >= 0.45 ? 'text-amber-400' : 'text-rose-400';
  const isUntrained = detail.status === 'baseline_untrained' || detail.status === 'untrained_baseline';

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <header className="space-y-2">
        <Link href="/candidates" className="text-sm text-indigo-400 hover:text-indigo-300 transition flex items-center gap-1">
          ← Back to Candidates
        </Link>
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-slate-100">{detail.targetName}</h1>
            <p className="text-slate-400 mt-1 max-w-lg text-sm">{detail.shortSummary ?? 'No target summary available.'}</p>
          </div>
          <div className="flex items-center gap-3">
            <span className={`px-4 py-2 rounded-xl text-sm font-bold border ${
              isFP ? 'bg-rose-500/10 text-rose-400 border-rose-500/30' : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
            }`}>
              {detail.label}
            </span>
          </div>
        </div>
      </header>

      {/* Score Hero */}
      <div className="glass rounded-2xl p-6 flex flex-col md:flex-row items-center gap-6">
        <div className="text-center">
          <div className="text-xs text-slate-500 uppercase tracking-wider mb-1">AstroNet Score</div>
          <div className={`text-6xl font-bold font-mono ${scoreColor}`}>
            {detail.astronet_score.toFixed(3)}
          </div>
          <div className="text-xs text-slate-500 mt-2">0.0 = FP · 1.0 = Planet</div>
        </div>
        <div className="flex-1 w-full">
          <div className="w-full h-3 bg-slate-800 rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full transition-all ${detail.astronet_score >= 0.7 ? 'bg-emerald-500' : detail.astronet_score >= 0.45 ? 'bg-amber-500' : 'bg-rose-500'}`}
              style={{ width: `${detail.astronet_score * 100}%` }}
            />
          </div>
          <div className="flex justify-between text-xs text-slate-600 mt-1">
            <span>0 — False Positive</span>
            <span>1 — Planet Candidate</span>
          </div>
          {isUntrained && (
            <div className="mt-3 text-xs text-amber-400 bg-amber-500/5 border border-amber-500/20 px-3 py-2 rounded-lg">
              ⚠️ Score is at untrained baseline (~0.5). Will update after model training.
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Physical Parameters */}
        <div className="glass rounded-2xl p-6">
          <h2 className="text-lg font-bold text-slate-200 mb-4">Physical Parameters</h2>
          <MetricRow label="BLS Period" value={`${detail.bls_period.toFixed(4)} days`} mono />
          <MetricRow label="Transit Midpoint (T0)" value={detail.bls_t0 !== undefined ? `${detail.bls_t0.toFixed(4)} BKJD` : 'N/A'} mono />
          <MetricRow label="Transit Duration" value={detail.bls_duration !== undefined ? `${(detail.bls_duration * 24).toFixed(2)} hours` : 'N/A'} mono />
          <MetricRow label="SNR" value={detail.snr.toFixed(2)} mono />
          <MetricRow label="Radius Ratio k (Rp/Rs)" value={detail.fitted_k.toFixed(4)} mono />
          <MetricRow label="Secondary Eclipse Depth" value={detail.secondary_eclipse_depth.toFixed(4)} mono />
        </div>

        {/* Vetting Summary */}
        <div className="glass rounded-2xl p-6">
          <h2 className="text-lg font-bold text-slate-200 mb-4">Vetting Summary</h2>
          <div className="space-y-3">
            <VettingCard
              ok={!detail.odd_even_suspicious}
              label="Odd-Even Test"
              detail={detail.odd_even_suspicious ? 'Depth asymmetry detected — possible eclipsing binary.' : 'Odd and even transit depths are consistent.'}
            />
            <VettingCard
              ok={detail.secondary_eclipse_depth < 0.001}
              label="Secondary Eclipse"
              detail={detail.secondary_eclipse_depth < 0.001 ? 'No significant secondary eclipse found.' : `Secondary eclipse detected at depth ${detail.secondary_eclipse_depth.toFixed(4)}.`}
            />
            <VettingCard
              ok={detail.snr >= 7.1}
              label="SNR Threshold"
              detail={detail.snr >= 7.1 ? `SNR ${detail.snr.toFixed(1)} exceeds 7.1σ detection threshold.` : `SNR ${detail.snr.toFixed(1)} is below 7.1σ. May be marginal signal.`}
            />
            <VettingCard
              ok={!isUntrained}
              label="Model Training Status"
              detail={isUntrained ? 'Model not yet trained. Score is random baseline.' : 'Score from trained model.'}
            />
          </div>
        </div>
      </div>

      {/* Plots */}
      <div className="glass rounded-2xl p-6">
        <h2 className="text-lg font-bold text-slate-200 mb-4">Light Curve Analysis</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <div className="text-sm font-medium text-slate-400 mb-2">Phase-Folded Light Curve</div>
            <div className="bg-slate-900/50 rounded-xl overflow-hidden border border-slate-800/50 aspect-video flex items-center justify-center">
              {detail.foldedPlot ? (
                <PlotImage
                  src={detail.foldedPlot}
                  alt={`Phase-folded light curve for ${detail.targetName}`}
                  className="w-full h-full object-contain"
                />
              ) : (
                <div className="text-center text-slate-600 text-sm p-8">
                  <div className="text-3xl mb-2">📊</div>
                  Plot pending pipeline run
                </div>
              )}
            </div>
          </div>
          <div>
            <div className="text-sm font-medium text-slate-400 mb-2">Diagnostic / Vetting Plot</div>
            <div className="bg-slate-900/50 rounded-xl overflow-hidden border border-slate-800/50 aspect-video flex items-center justify-center">
              {detail.diagnosticPlot ? (
                <PlotImage
                  src={detail.diagnosticPlot}
                  alt={`Diagnostic plot for ${detail.targetName}`}
                  className="w-full h-full object-contain"
                />
              ) : (
                <div className="text-center text-slate-600 text-sm p-8">
                  <div className="text-3xl mb-2">🔬</div>
                  Plot pending pipeline run
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
