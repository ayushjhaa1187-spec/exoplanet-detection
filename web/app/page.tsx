import StatsCard from '@/components/dashboard/StatsCard';
import PipelineFlow from '@/components/dashboard/PipelineFlow';
import { ModelMetrics } from '@/lib/types';
import fs from 'fs';
import path from 'path';

export default async function Home() {
  // Read metrics data
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
        <h1 className="text-3xl font-bold">Project Overview</h1>
        <p className="text-slate-400 mt-2">End-to-end exoplanet detection, classification, and scientific validation.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard title="Analyzed Candidates" value={metrics?.datasetSize || 0} description="Light curves fetched and processed" />
        <StatsCard title="Model Accuracy" value={`${((metrics?.accuracy || 0) * 100).toFixed(1)}%`} description="Validation performance" />
        <StatsCard title="Precision" value={`${((metrics?.precision || 0) * 100).toFixed(1)}%`} description="False positive resistance" />
        <StatsCard title="Experiment" value={metrics?.experimentName || 'N/A'} description="Current active model" />
      </div>

      <PipelineFlow />

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h3 className="text-lg font-bold mb-4">Scientific Context</h3>
        <p className="text-sm text-slate-300 leading-relaxed">
          This platform utilizes an <strong>Advanced AstroNet CNN</strong> featuring ExoMiner-style Multi-Head Attention blocks 
          to classify transit events from Kepler and TESS light curves. Beyond standard classification, candidates undergo 
          rigorous physical validation (SNR thresholds, Odd-Even consistency checks) and are ultimately fitted using 
          <strong> PyTransit</strong> to extract scientific parameters like the planetary radius ratio.
        </p>
      </div>
    </div>
  );
}
