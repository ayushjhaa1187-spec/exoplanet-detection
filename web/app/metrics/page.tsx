import fs from 'fs';
import path from 'path';

type Metrics = {
  experimentName?: string;
  accuracy?: number;
  precision?: number;
  recall?: number;
  f1?: number;
  auc?: number;
  datasetSize?: number;
  notes?: string;
};

export default async function MetricsPage() {
  const dataPath = path.join(process.cwd(), 'public/data/metrics.json');
  let metrics: Metrics = {};
  try {
    metrics = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
  } catch (e) {
    console.error('Could not load metrics:', e);
  }

  const metricCards = [
    { label: 'Accuracy', value: metrics.accuracy, color: 'indigo' },
    { label: 'Precision', value: metrics.precision, color: 'violet' },
    { label: 'Recall', value: metrics.recall, color: 'purple' },
    { label: 'F1 Score', value: metrics.f1, color: 'fuchsia' },
  ];

  return (
    <div className="space-y-8">
      <header className="space-y-1">
        <h1 className="text-3xl font-bold tracking-tight">Model Metrics</h1>
        <p className="text-slate-400">
          {metrics.experimentName ?? 'No experiment data yet.'}
        </p>
      </header>

      {/* Status Banner */}
      <div className="flex items-start gap-3 px-4 py-3 rounded-xl bg-amber-500/5 border border-amber-500/20 text-amber-300 text-sm">
        <span className="text-lg mt-0.5">⚠️</span>
        <div>
          <strong>Model not yet trained.</strong> Metrics below are from a prototype run on a small dataset (6 samples).
          Train on the full Kepler DR24 TCE dataset (~15k samples) to get real performance numbers.
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {metricCards.map(({ label, value }) => (
          <div key={label} className="glass rounded-2xl p-6 text-center">
            <div className="text-xs text-slate-500 uppercase tracking-wider mb-2">{label}</div>
            <div className="text-4xl font-bold text-slate-100">
              {value !== undefined ? `${(value * 100).toFixed(1)}%` : '—'}
            </div>
          </div>
        ))}
      </div>

      {/* Details */}
      <div className="glass rounded-2xl p-8">
        <h2 className="text-lg font-bold text-slate-200 mb-4">Experiment Details</h2>
        <div className="space-y-3 text-sm">
          <div className="flex justify-between py-2 border-b border-slate-800/50">
            <span className="text-slate-400">Dataset Size</span>
            <span className="font-mono text-slate-200">{metrics.datasetSize ?? 'N/A'} samples</span>
          </div>
          <div className="flex justify-between py-2 border-b border-slate-800/50">
            <span className="text-slate-400">AUC-ROC</span>
            <span className="font-mono text-slate-200">{metrics.auc ? metrics.auc.toFixed(3) : 'N/A'}</span>
          </div>
          <div className="flex justify-between py-2">
            <span className="text-slate-400">Notes</span>
            <span className="text-slate-300 max-w-sm text-right">{metrics.notes ?? '—'}</span>
          </div>
        </div>
      </div>

      {/* Next Steps */}
      <div className="glass rounded-2xl p-8">
        <h2 className="text-lg font-bold text-slate-200 mb-4">🚀 Next Steps to Get Real Metrics</h2>
        <ol className="space-y-3 text-sm text-slate-400 list-none">
          {[
            'Download Kepler DR24 TCE catalog (~15,000 threshold crossing events)',
            'Run scripts/train_baseline.py — trains AstroNet for 20 epochs',
            'Export metrics.json and astronet_weights.h5',
            'Re-run pipeline — scores will change from 0.5 to real predictions',
            'Deploy updated candidates.json to this dashboard',
          ].map((step, i) => (
            <li key={i} className="flex items-start gap-3">
              <span className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-900/40 border border-indigo-700/40 text-indigo-400 text-xs font-bold flex items-center justify-center">
                {i + 1}
              </span>
              {step}
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
