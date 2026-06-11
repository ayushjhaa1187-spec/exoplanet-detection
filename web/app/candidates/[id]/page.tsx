import { CandidateDetail } from '@/lib/types';
import fs from 'fs';
import path from 'path';
import Link from 'next/link';

export default async function CandidateDetailPage({ params }: { params: { id: string } }) {
  const dataPath = path.join(process.cwd(), `public/data/candidate_${params.id}.json`);
  let detail: CandidateDetail | null = null;
  
  try {
    const fileContents = fs.readFileSync(dataPath, 'utf8');
    detail = JSON.parse(fileContents);
  } catch (err) {
    console.error(err);
  }

  if (!detail) {
    return (
      <div className="text-center py-20">
        <h2 className="text-2xl font-bold">Candidate not found</h2>
        <Link href="/candidates" className="text-indigo-400 mt-4 inline-block">&larr; Back to list</Link>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-12">
      <header className="flex items-center justify-between">
        <div>
          <Link href="/candidates" className="text-sm text-indigo-400 hover:underline mb-2 inline-block">&larr; Back to Candidates</Link>
          <h1 className="text-3xl font-bold flex items-center gap-4">
            {detail.targetName}
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${detail.label === 'Confirmed Planet' ? 'bg-emerald-900/30 text-emerald-400 border border-emerald-800' : 'bg-rose-900/30 text-rose-400 border border-rose-800'}`}>
              {detail.label}
            </span>
          </h1>
          <p className="text-slate-400 mt-2">{detail.shortSummary}</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-slate-500">Model Confidence</p>
          <p className="text-4xl font-bold text-white">{(detail.confidence * 100).toFixed(1)}%</p>
        </div>
      </header>

      {/* Vetting Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-4">
          <p className="text-xs text-slate-500">Orbital Period</p>
          <p className="text-lg font-semibold">{detail.period.toFixed(4)} d</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-4">
          <p className="text-xs text-slate-500">Signal-to-Noise (SNR)</p>
          <p className="text-lg font-semibold">{detail.snr.toFixed(1)}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-4">
          <p className="text-xs text-slate-500">Radius Ratio (k)</p>
          <p className="text-lg font-semibold">{detail.radiusRatio.toFixed(4)}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-4">
          <p className="text-xs text-slate-500">Odd-Even Suspicious</p>
          <p className={`text-lg font-semibold ${detail.oddEvenSuspicious ? 'text-rose-400' : 'text-emerald-400'}`}>
            {detail.oddEvenSuspicious ? 'Yes' : 'No'}
          </p>
        </div>
      </div>

      {/* Plots */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden flex flex-col">
          <div className="p-4 border-b border-slate-800 bg-slate-800/30">
            <h3 className="font-semibold text-slate-200">Phase-Folded Light Curve</h3>
            <p className="text-xs text-slate-500 mt-1">AstroNet local view context</p>
          </div>
          <div className="p-4 flex-1 flex items-center justify-center bg-white/5">
            {/* Using a placeholder visual if actual plot is missing during dev */}
            <img src={detail.foldedPlot} alt="Folded Plot" className="w-full h-auto rounded object-cover" 
                 onError={(e) => { e.currentTarget.src = 'https://via.placeholder.com/600x400/1e293b/a5b4fc?text=Phase-Folded+Plot+Not+Found' }} />
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden flex flex-col">
          <div className="p-4 border-b border-slate-800 bg-slate-800/30">
            <h3 className="font-semibold text-slate-200">PyTransit Scientific Fit</h3>
            <p className="text-xs text-slate-500 mt-1">RoadRunner analytical transit model</p>
          </div>
          <div className="p-4 flex-1 flex items-center justify-center bg-white/5">
            <img src={detail.transitFitPlot || detail.foldedPlot} alt="Transit Fit Plot" className="w-full h-auto rounded object-cover"
                 onError={(e) => { e.currentTarget.src = 'https://via.placeholder.com/600x400/1e293b/a5b4fc?text=PyTransit+Fit+Not+Found' }} />
          </div>
        </div>
      </div>

    </div>
  );
}
