import { getMetrics } from '@/lib/data';

export default async function MetricsPage() {
  const metrics = await getMetrics();

  const metricCards = [
    { label: 'Accuracy', value: metrics.accuracy },
    { label: 'Precision', value: metrics.precision },
    { label: 'Recall', value: metrics.recall },
    { label: 'F1 Score', value: metrics.f1 },
  ];

  return (
    <div className="space-y-8 py-4">
      <header className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight text-text-primary">Model Metrics</h1>
        <p className="text-text-secondary text-lg">
          {metrics.experimentName ?? 'No experiment data yet.'}
        </p>
      </header>

      {/* Status Banner */}
      <div className="flex items-start gap-3 px-5 py-4 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-sm">
        <span className="text-lg mt-0.5">⚠️</span>
        <div>
          <strong className="font-semibold block mb-1">Model not yet trained.</strong> 
          <span className="text-amber-700/90">Metrics below are from a prototype run on a small dataset (6 samples).
          Train on the full Kepler DR24 TCE dataset (~15k samples) to get real performance numbers.</span>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        {metricCards.map(({ label, value }) => (
          <div key={label} className="card p-6 text-center hover:border-brand-primary/30 transition-colors">
            <div className="text-xs text-text-secondary uppercase tracking-wider mb-3 font-semibold">{label}</div>
            <div className="text-4xl font-bold text-text-primary">
              {value !== undefined ? `${(value * 100).toFixed(1)}%` : '—'}
            </div>
          </div>
        ))}
      </div>

      {/* Details */}
      <div className="card p-8 bg-surface-alt/30 border-l-4 border-l-brand-secondary">
        <h2 className="text-lg font-bold text-text-primary mb-4 border-b border-border-subtle pb-2">Experiment Details</h2>
        <div className="space-y-1 text-sm">
          <div className="flex justify-between py-3 border-b border-border-subtle">
            <span className="text-text-secondary">Dataset Size</span>
            <span className="font-mono text-text-primary font-medium">{metrics.datasetSize ?? 'N/A'} samples</span>
          </div>
          <div className="flex justify-between py-3 border-b border-border-subtle">
            <span className="text-text-secondary">AUC-ROC</span>
            <span className="font-mono text-text-primary font-medium">{metrics.auc ? metrics.auc.toFixed(3) : 'N/A'}</span>
          </div>
          <div className="flex justify-between py-3">
            <span className="text-text-secondary">Notes</span>
            <span className="text-text-secondary max-w-sm text-right leading-relaxed">{metrics.notes ?? '—'}</span>
          </div>
        </div>
      </div>

      {/* Next Steps */}
      <div className="card p-8">
        <h2 className="text-lg font-bold text-text-primary mb-6 flex items-center gap-2">
          🚀 Next Steps to Get Real Metrics
        </h2>
        <ol className="space-y-4 text-sm text-text-secondary list-none">
          {[
            'Download Kepler DR24 TCE catalog (~15,000 threshold crossing events)',
            'Run scripts/train_baseline.py — trains AstroNet for 20 epochs',
            'Export metrics.json and astronet_weights.h5',
            'Re-run pipeline — scores will change from 0.5 to real predictions',
            'Deploy updated candidates.json to this dashboard',
          ].map((step, i) => (
            <li key={i} className="flex items-start gap-4 p-3 rounded-lg hover:bg-surface-alt transition-colors border border-transparent hover:border-border-subtle">
              <span className="flex-shrink-0 w-7 h-7 rounded-full bg-brand-primary/10 border border-brand-primary/20 text-brand-primary text-xs font-bold flex items-center justify-center">
                {i + 1}
              </span>
              <span className="pt-1">{step}</span>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
