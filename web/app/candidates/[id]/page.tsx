import Link from 'next/link';
import { notFound } from 'next/navigation';
import PlotImage from '@/components/PlotImage';
import { getCandidateById } from '@/lib/data';

type PageParams = Promise<{ id: string }>;

function VettingCard({ ok, label, detail }: { ok: boolean; label: string; detail: string }) {
  return (
    <div className={`flex items-start gap-3 p-4 rounded-xl border ${
      ok ? 'bg-emerald-50 border-emerald-200' : 'bg-rose-50 border-rose-200'
    }`}>
      <span className="text-lg mt-0.5">{ok ? '✅' : '⚠️'}</span>
      <div>
        <div className={`text-sm font-semibold ${ok ? 'text-emerald-800' : 'text-rose-800'}`}>{label}</div>
        <div className={`text-xs mt-0.5 ${ok ? 'text-emerald-700/80' : 'text-rose-700/80'}`}>{detail}</div>
      </div>
    </div>
  );
}

function MetricRow({ label, value, mono }: { label: string; value: string; mono?: boolean }) {
  return (
    <div className="flex items-center justify-between py-3 border-b border-border-subtle last:border-0">
      <span className="text-sm text-text-secondary">{label}</span>
      <span className={`text-sm font-semibold text-text-primary ${mono ? 'font-mono' : ''}`}>{value}</span>
    </div>
  );
}

export default async function CandidateDetailPage({ params }: { params: PageParams }) {
  const { id } = await params;
  const detail = await getCandidateById(id);
  if (!detail) notFound();

  const effectiveLabel = detail.classification || detail.label || 'Unknown';
  const isFP = effectiveLabel.toLowerCase().includes('false') || effectiveLabel.toLowerCase().includes('suspect') || effectiveLabel.toLowerCase().includes('noise') || effectiveLabel.toLowerCase().includes('blend') || effectiveLabel.toLowerCase().includes('eclipse');
  const score = detail.confidence ?? detail.astronet_score ?? 0;
  const scoreColor = score >= 0.7 ? 'text-emerald-600' : score >= 0.45 ? 'text-amber-600' : 'text-rose-600';
  const isUntrained = detail.status === 'baseline_untrained' || detail.status === 'untrained_baseline';

  return (
    <div className="space-y-8 pb-12 py-4">
      {/* Header */}
      <header className="space-y-2">
        <Link href="/candidates" className="text-sm text-brand-primary hover:text-brand-secondary transition flex items-center gap-1 font-medium">
          ← Back to Candidates
        </Link>
        <div className="flex items-start justify-between gap-4 flex-wrap pt-2">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-text-primary">{detail.targetName}</h1>
            <p className="text-text-secondary mt-1 max-w-lg text-sm">{detail.shortSummary ?? 'No target summary available.'}</p>
          </div>
          <div className="flex items-center gap-3">
            <span className={`px-4 py-2 rounded-xl text-sm font-bold border ${
              isFP ? 'bg-rose-50 text-rose-700 border-rose-200' : 'bg-emerald-50 text-emerald-700 border-emerald-200'
            }`}>
              {effectiveLabel}
            </span>
          </div>
        </div>
      </header>

      {/* Score Hero */}
      <div className="card p-8 flex flex-col md:flex-row items-center gap-8 border-t-4 border-t-brand-primary">
        <div className="text-center md:min-w-[200px]">
          <div className="text-xs text-text-secondary uppercase tracking-wider mb-2 font-semibold">Confidence Score</div>
          <div className={`text-6xl font-bold font-mono ${scoreColor}`}>
            {score.toFixed(3)}
          </div>
          <div className="text-xs text-text-secondary mt-3">0.0 = Low · 1.0 = High</div>
        </div>
        <div className="flex-1 w-full bg-surface-alt rounded-2xl p-6 border border-border-subtle">
          <div className="flex justify-between text-xs text-text-secondary mb-2 font-medium">
            <span>0.0 (Low Confidence)</span>
            <span>1.0 (High Confidence)</span>
          </div>
          <div className="w-full h-4 bg-border-subtle rounded-full overflow-hidden mb-2">
            <div
              className={`h-full rounded-full transition-all ${score >= 0.7 ? 'bg-emerald-500' : score >= 0.45 ? 'bg-amber-500' : 'bg-rose-500'}`}
              style={{ width: `${score * 100}%` }}
            />
          </div>
          
          {isUntrained && (
            <div className="mt-4 text-xs text-amber-800 bg-amber-50 border border-amber-200 px-4 py-3 rounded-xl font-medium">
              ⚠️ Score is at untrained baseline (~0.5). Will update after model training.
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Physical Parameters */}
        <div className="card p-6">
          <h2 className="text-lg font-bold text-text-primary mb-4 border-b border-border-subtle pb-2">Physical Parameters</h2>
          <MetricRow label="BLS Period" value={`${detail.bls_period.toFixed(4)} days`} mono />
          <MetricRow label="Transit Midpoint (T0)" value={detail.bls_t0 !== undefined ? `${detail.bls_t0.toFixed(4)} BKJD` : 'N/A'} mono />
          <MetricRow label="Transit Duration" value={detail.bls_duration !== undefined ? `${(detail.bls_duration * 24).toFixed(2)} hours` : 'N/A'} mono />
          <MetricRow label="Signal-to-Noise (SNR)" value={detail.snr.toFixed(2)} mono />
          <MetricRow label="Radius Ratio k (Rp/Rs)" value={detail.fitted_k.toFixed(4)} mono />
          <MetricRow label="Secondary Eclipse Depth" value={detail.secondary_eclipse_depth.toFixed(4)} mono />
        </div>

        {/* Vetting Summary */}
        <div className="card p-6 bg-surface-alt/30">
          <h2 className="text-lg font-bold text-text-primary mb-4 border-b border-border-subtle pb-2">Vetting Summary</h2>
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
      <div className="card p-6">
        <h2 className="text-lg font-bold text-text-primary mb-6 border-b border-border-subtle pb-2">Light Curve Analysis</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <div className="text-sm font-semibold text-text-secondary mb-3 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-brand-primary"></span>
              Phase-Folded Light Curve
            </div>
            <div className="bg-white rounded-xl overflow-hidden border border-border-subtle aspect-video flex items-center justify-center shadow-sm">
              {detail.foldedPlot ? (
                <PlotImage
                  src={detail.foldedPlot}
                  alt={`Phase-folded light curve for ${detail.targetName}`}
                  className="w-full h-full object-contain"
                />
              ) : (
                <div className="text-center text-text-secondary text-sm p-8">
                  <div className="text-3xl mb-3 opacity-50">📊</div>
                  Plot pending pipeline run
                </div>
              )}
            </div>
          </div>
          <div>
            <div className="text-sm font-semibold text-text-secondary mb-3 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-brand-secondary"></span>
              Diagnostic / Vetting Plot
            </div>
            <div className="bg-white rounded-xl overflow-hidden border border-border-subtle aspect-video flex items-center justify-center shadow-sm">
              {detail.diagnosticPlot ? (
                <PlotImage
                  src={detail.diagnosticPlot}
                  alt={`Diagnostic plot for ${detail.targetName}`}
                  className="w-full h-full object-contain"
                />
              ) : (
                <div className="text-center text-text-secondary text-sm p-8">
                  <div className="text-3xl mb-3 opacity-50">🔬</div>
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
