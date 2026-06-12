import Link from 'next/link';

const stats = [
  { label: 'Stars Analyzed', value: '10', icon: '⭐', sub: 'Kepler targets' },
  { label: 'Candidates Found', value: '5', icon: '🪐', sub: 'Classified by CNN' },
  { label: 'Model Accuracy', value: 'Training...', icon: '🤖', sub: 'Awaiting training' },
  { label: 'Pipeline Stages', value: '5', icon: '🔬', sub: 'End-to-end' },
];

const pipelineSteps = [
  { num: 1, name: 'Fetch', desc: 'Lightkurve + MAST', icon: '📡' },
  { num: 2, name: 'Preprocess', desc: 'Global/Local binning', icon: '⚙️' },
  { num: 3, name: 'CNN', desc: 'AstroNet + Attention', icon: '🧠' },
  { num: 4, name: 'Vet', desc: 'SNR + Odd-Even', icon: '🔍' },
  { num: 5, name: 'Fit', desc: 'PyTransit model', icon: '📈' },
];

const recentCandidates = [
  { id: 'kepler-22b', name: 'Kepler-22b', score: 0.4998, period: 16.774, snr: 2.53, label: 'PLANET CANDIDATE', status: 'baseline_untrained' },
];

export default function HomePage() {
  return (
    <div className="space-y-16 py-4">
      {/* Hero */}
      <section className="text-center space-y-6 pt-12 pb-8">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-brand-primary/10 border border-brand-primary/20 text-brand-primary text-sm font-medium mb-2">
          <span className="w-1.5 h-1.5 rounded-full bg-brand-primary animate-pulse" />
          Live Pipeline — Kepler Data
        </div>
        <h1 className="text-5xl md:text-6xl font-bold tracking-tight leading-tight">
          AI-Powered
          <br />
          <span className="text-brand-primary">Exoplanet Detection</span>
        </h1>
        <p className="text-text-secondary text-lg max-w-xl mx-auto leading-relaxed">
          From raw Kepler light curves to vetted planet candidates — using an AstroNet CNN
          with Multi-Head Attention and PyTransit scientific fitting.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
          <Link
            href="/candidates"
            id="btn-view-candidates"
            className="px-6 py-3 rounded-xl bg-brand-primary hover:bg-[#4a1b94] text-white font-medium transition-all duration-200 shadow-lg shadow-brand-primary/20 hover:-translate-y-0.5"
          >
            View Candidates →
          </Link>
          <Link
            href="/about"
            id="btn-see-pipeline"
            className="px-6 py-3 rounded-xl border border-border-subtle hover:border-brand-primary/50 text-text-primary font-medium transition-all duration-200 bg-surface-card hover:shadow-sm"
          >
            Pipeline Details
          </Link>
        </div>
      </section>

      {/* Stats */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((s) => (
          <div
            key={s.label}
            className="card p-6 text-center hover:border-brand-primary/30 transition-all duration-300 group"
          >
            <div className="text-3xl mb-3 group-hover:scale-110 transition-transform duration-200">{s.icon}</div>
            <div className="text-3xl font-bold text-text-primary mb-1">{s.value}</div>
            <div className="text-sm font-medium text-text-secondary">{s.label}</div>
            <div className="text-xs text-text-secondary/70 mt-1">{s.sub}</div>
          </div>
        ))}
      </section>

      {/* Pipeline Flow */}
      <section className="card p-8">
        <h2 className="text-xl font-bold text-text-primary mb-8 text-center">Pipeline Flow</h2>
        <div className="flex flex-col md:flex-row items-center gap-4 md:gap-0">
          {pipelineSteps.map((step, idx) => (
            <div key={step.num} className="flex flex-row md:flex-col items-center gap-4 md:gap-0 flex-1 w-full md:w-auto">
              <div className="flex flex-col md:flex-col items-center flex-1">
                <div className="w-14 h-14 rounded-2xl bg-surface-alt border border-border-subtle flex items-center justify-center text-xl shadow-sm hover:scale-105 hover:border-brand-secondary/50 hover:bg-brand-secondary/5 transition-all duration-200">
                  {step.icon}
                </div>
                <div className="mt-4 text-center">
                  <div className="text-sm font-semibold text-text-primary">{step.name}</div>
                  <div className="text-xs text-text-secondary mt-1">{step.desc}</div>
                </div>
              </div>
              {idx < pipelineSteps.length - 1 && (
                <div className="hidden md:flex text-border-subtle text-2xl mt-0 mx-2 items-center self-start pt-3">→</div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* Recent Candidates */}
      <section>
        <div className="flex items-center justify-between mb-4 px-1">
          <h2 className="text-xl font-bold text-text-primary">Recent Candidates</h2>
          <Link href="/candidates" className="text-sm text-brand-primary font-medium hover:underline transition">
            View all →
          </Link>
        </div>
        <div className="card overflow-hidden">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-border-subtle text-xs font-semibold text-text-secondary uppercase tracking-wider bg-surface-alt/50">
                <th className="px-6 py-4">Target</th>
                <th className="px-6 py-4">AstroNet Score</th>
                <th className="px-6 py-4 text-right">Period (d)</th>
                <th className="px-6 py-4 text-right">SNR</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle">
              {recentCandidates.map((c) => (
                <tr key={c.id} className="hover:bg-surface-alt transition-colors duration-150 group">
                  <td className="px-6 py-4">
                    <span className="font-semibold text-text-primary">{c.name}</span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="flex-1 max-w-24 h-1.5 bg-border-subtle rounded-full overflow-hidden">
                        <div
                          className="h-full bg-brand-primary rounded-full transition-all"
                          style={{ width: `${c.score * 100}%` }}
                        />
                      </div>
                      <span className="text-sm text-text-secondary font-mono">{c.score.toFixed(3)}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 font-mono text-sm text-text-secondary text-right">{c.period.toFixed(2)}</td>
                  <td className="px-6 py-4 font-mono text-sm text-text-secondary text-right">{c.snr.toFixed(1)}</td>
                  <td className="px-6 py-4">
                    <span className="status-uncertain">
                      {c.status === 'untrained' ? 'Baseline (untrained)' : c.label}
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
      </section>

      {/* Scientific Context */}
      <section className="card p-8 border-l-4 border-l-brand-primary">
        <h2 className="text-lg font-bold text-text-primary mb-3">Scientific Context</h2>
        <p className="text-text-secondary text-sm leading-relaxed max-w-4xl">
          This platform uses an <strong className="text-text-primary font-semibold">Advanced AstroNet CNN</strong> with ExoMiner-style
          Multi-Head Attention blocks to classify transit events from Kepler light curves. Candidates undergo rigorous
          physical validation — SNR threshold checks, odd-even depth consistency tests, secondary eclipse detection —
          and are fitted using <strong className="text-text-primary font-semibold">PyTransit</strong> (RoadRunner model) to extract
          scientific parameters like the planetary radius ratio <em>k = R&#8346;/R&#8346;</em>.
        </p>
        <div className="mt-5 flex flex-wrap gap-2">
          {['Lightkurve', 'TensorFlow / Keras', 'PyTransit', 'BLS Periodogram', 'AstroNet CNN', 'Multi-Head Attention'].map((tag) => (
            <span key={tag} className="px-3 py-1 rounded-md text-xs font-medium bg-surface-alt text-text-secondary border border-border-subtle">
              {tag}
            </span>
          ))}
        </div>
      </section>
    </div>
  );
}
