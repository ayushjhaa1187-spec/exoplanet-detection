import Link from 'next/link';

const stats = [
  { label: 'Stars Analyzed', value: '12', icon: '⭐', sub: 'Kepler targets' },
  { label: 'Candidates Found', value: '5', icon: '🪐', sub: 'Classified by CNN' },
  { label: 'Model Accuracy', value: 'TBD', icon: '🤖', sub: 'Awaiting training' },
  { label: 'Pipeline Stages', value: '5', icon: '🔬', sub: 'End-to-end' },
];

const pipelineSteps = [
  { num: 1, name: 'Fetch', desc: 'Lightkurve + MAST', icon: '📡', color: 'from-blue-600 to-blue-500' },
  { num: 2, name: 'Preprocess', desc: 'Global/Local binning', icon: '⚙️', color: 'from-violet-600 to-violet-500' },
  { num: 3, name: 'CNN Classify', desc: 'AstroNet + Attention', icon: '🧠', color: 'from-indigo-600 to-indigo-500' },
  { num: 4, name: 'Vet', desc: 'SNR + Odd-Even', icon: '🔍', color: 'from-purple-600 to-purple-500' },
  { num: 5, name: 'Fit Transit', desc: 'PyTransit model', icon: '📈', color: 'from-fuchsia-600 to-fuchsia-500' },
];

const recentCandidates = [
  { id: 'kepler-22b', name: 'Kepler-22b', score: 0.50, period: 16.77, snr: 2.53, label: 'PLANET CANDIDATE', status: 'untrained' },
  { id: 'kepler-10b', name: 'Kepler-10b', score: 0.50, period: 0.84, snr: 16.2, label: 'PLANET CANDIDATE', status: 'untrained' },
  { id: 'kepler-452b', name: 'Kepler-452b', score: 0.50, period: 384.8, snr: 10.5, label: 'PLANET CANDIDATE', status: 'untrained' },
];

export default function HomePage() {
  return (
    <div className="space-y-16 py-4">
      {/* Hero */}
      <section className="text-center space-y-6 pt-8 pb-4">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-sm font-medium mb-2">
          <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse" />
          Live Pipeline — Kepler Data
        </div>
        <h1 className="text-5xl md:text-6xl font-bold tracking-tight leading-tight">
          <span className="text-gradient">AI-Powered</span>
          <br />
          <span className="text-slate-100">Exoplanet Detection</span>
        </h1>
        <p className="text-slate-400 text-lg max-w-xl mx-auto leading-relaxed">
          From raw Kepler light curves to vetted planet candidates — using an AstroNet CNN
          with Multi-Head Attention and PyTransit scientific fitting.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
          <Link
            href="/candidates"
            id="btn-view-candidates"
            className="px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold transition-all duration-200 shadow-lg shadow-indigo-900/40 hover:shadow-indigo-900/60 hover:-translate-y-0.5 active:translate-y-0"
          >
            View Candidates →
          </Link>
          <Link
            href="/about"
            id="btn-see-pipeline"
            className="px-6 py-3 rounded-xl border border-slate-700 hover:border-indigo-500/60 text-slate-300 hover:text-indigo-300 font-medium transition-all duration-200 hover:-translate-y-0.5 active:translate-y-0"
          >
            See Pipeline
          </Link>
        </div>
      </section>

      {/* Stats */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((s) => (
          <div
            key={s.label}
            className="glass rounded-2xl p-5 text-center hover:glow-indigo transition-all duration-300 group"
          >
            <div className="text-3xl mb-3 group-hover:scale-110 transition-transform duration-200">{s.icon}</div>
            <div className="text-3xl font-bold text-white mb-1">{s.value}</div>
            <div className="text-sm font-medium text-slate-300">{s.label}</div>
            <div className="text-xs text-slate-500 mt-1">{s.sub}</div>
          </div>
        ))}
      </section>

      {/* Pipeline Flow */}
      <section className="glass rounded-2xl p-8">
        <h2 className="text-xl font-bold text-slate-200 mb-6 text-center">Pipeline Flow</h2>
        <div className="flex flex-col md:flex-row items-center gap-2 md:gap-0">
          {pipelineSteps.map((step, idx) => (
            <div key={step.num} className="flex flex-row md:flex-col items-center gap-2 md:gap-0 flex-1 w-full md:w-auto">
              <div className="flex flex-col md:flex-col items-center flex-1">
                <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${step.color} flex items-center justify-center text-xl shadow-lg shadow-indigo-900/30 hover:scale-105 transition-transform duration-200`}>
                  {step.icon}
                </div>
                <div className="mt-3 text-center">
                  <div className="text-sm font-semibold text-slate-200">{step.name}</div>
                  <div className="text-xs text-slate-500 mt-0.5">{step.desc}</div>
                </div>
              </div>
              {idx < pipelineSteps.length - 1 && (
                <div className="hidden md:flex text-slate-600 text-xl mt-0 mx-2 items-center self-start pt-4">→</div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* Recent Candidates */}
      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-slate-200">Recent Candidates</h2>
          <Link href="/candidates" className="text-sm text-indigo-400 hover:text-indigo-300 transition">
            View all →
          </Link>
        </div>
        <div className="glass rounded-2xl overflow-hidden">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-slate-800/60 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                <th className="px-6 py-4">Target</th>
                <th className="px-6 py-4">AstroNet Score</th>
                <th className="px-6 py-4">Period (d)</th>
                <th className="px-6 py-4">SNR</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/40">
              {recentCandidates.map((c) => (
                <tr key={c.id} className="hover:bg-slate-800/20 transition-colors duration-150 group">
                  <td className="px-6 py-4">
                    <span className="font-semibold text-slate-200">{c.name}</span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 max-w-20 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-indigo-500 rounded-full transition-all"
                          style={{ width: `${c.score * 100}%` }}
                        />
                      </div>
                      <span className="text-sm text-slate-300 font-mono">{c.score.toFixed(3)}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 font-mono text-sm text-slate-300">{c.period.toFixed(2)}</td>
                  <td className="px-6 py-4 font-mono text-sm text-slate-300">{c.snr.toFixed(1)}</td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-0.5 rounded text-xs font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20">
                      {c.status === 'untrained' ? 'Baseline (untrained)' : c.label}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Link
                      href={`/candidates/${c.id}`}
                      className="text-xs text-indigo-400 hover:text-indigo-300 opacity-0 group-hover:opacity-100 transition-all duration-150"
                    >
                      Details →
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Scientific Context */}
      <section className="glass rounded-2xl p-8">
        <h2 className="text-lg font-bold text-slate-200 mb-3">Scientific Context</h2>
        <p className="text-slate-400 text-sm leading-relaxed max-w-3xl">
          This platform uses an <strong className="text-slate-200">Advanced AstroNet CNN</strong> with ExoMiner-style
          Multi-Head Attention blocks to classify transit events from Kepler light curves. Candidates undergo rigorous
          physical validation — SNR threshold checks, odd-even depth consistency tests, secondary eclipse detection —
          and are fitted using <strong className="text-slate-200">PyTransit</strong> (RoadRunner model) to extract
          scientific parameters like the planetary radius ratio <em>k = R&#8346;/R&#8346;</em>.
        </p>
        <div className="mt-4 flex flex-wrap gap-2">
          {['Lightkurve', 'TensorFlow / Keras', 'PyTransit', 'BLS Periodogram', 'AstroNet CNN', 'Multi-Head Attention'].map((tag) => (
            <span key={tag} className="px-3 py-1 rounded-full text-xs font-medium bg-indigo-900/20 text-indigo-300 border border-indigo-800/30">
              {tag}
            </span>
          ))}
        </div>
      </section>
    </div>
  );
}
