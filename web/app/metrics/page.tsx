import fs from 'fs';
import path from 'path';
import { ModelMetrics } from '@/lib/types';
import StatsCard from '@/components/dashboard/StatsCard';

export default async function MetricsPage() {
  const metricsPath = path.join(process.cwd(), 'public/data/metrics.json');
  let metrics: ModelMetrics | null = null;
  try {
    const fileContents = fs.readFileSync(metricsPath, 'utf8');
    metrics = JSON.parse(fileContents);
  } catch (err) {
    console.error("Could not load metrics", err);
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <header>
        <h1 className="text-3xl font-bold">Model Metrics</h1>
        <p className="text-slate-400 mt-2">Performance evaluation of the active classification model.</p>
      </header>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h2 className="text-xl font-bold mb-2">{metrics?.experimentName || 'Current Model'}</h2>
        <p className="text-sm text-slate-400">{metrics?.notes || 'No description available.'}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard title="Accuracy" value={`${((metrics?.accuracy || 0) * 100).toFixed(1)}%`} description="Overall correctness" />
        <StatsCard title="Precision" value={`${((metrics?.precision || 0) * 100).toFixed(1)}%`} description="True positive rate" />
        <StatsCard title="Recall" value={`${((metrics?.recall || 0) * 100).toFixed(1)}%`} description="Sensitivity" />
        <StatsCard title="F1 Score" value={`${((metrics?.f1 || 0) * 100).toFixed(1)}%`} description="Harmonic mean" />
      </div>
      
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h3 className="text-lg font-bold mb-4">Scientific Validation</h3>
        <p className="text-sm text-slate-300 leading-relaxed mb-4">
          Accuracy alone is insufficient for exoplanet detection due to extreme class imbalance (mostly false positives). 
          Our platform mitigates this by applying secondary scientific validation (LATTE-style Odd-Even tests, secondary eclipse search) 
          and transit modeling (PyTransit) to all candidates flagged by the CNN.
        </p>
      </div>
    </div>
  );
}
