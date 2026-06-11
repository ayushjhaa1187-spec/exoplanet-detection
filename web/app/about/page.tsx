export default function AboutPage() {
  const pipelineStages = [
    {
      num: 1, name: 'Data Fetch', icon: '📡',
      what: 'Light curves are fetched from NASA MAST using the Lightkurve library.',
      built: 'Custom ExoplanetDataFetcher wrapper with search + bulk download.',
      source: 'Lightkurve (open source), MAST archive (public)',
    },
    {
      num: 2, name: 'BLS Search', icon: '🔎',
      what: 'Box Least Squares (BLS) periodogram finds the strongest periodic transit signal.',
      built: 'Lightkurve BLS with 10,000-point period grid from 0.5 to 20 days.',
      source: 'BLS algorithm (Kovács et al. 2002)',
    },
    {
      num: 3, name: 'Preprocessing', icon: '⚙️',
      what: 'Light curve is phase-folded and binned into global (2001-bin) and local (201-bin) views.',
      built: 'Custom ExoplanetPreprocessor with median-aggregation binning + augmentation.',
      source: 'AstroNet paper (Shallue & Vanderburg 2018)',
    },
    {
      num: 4, name: 'CNN Classification', icon: '🧠',
      what: 'Dual-branch 1D CNN classifies the transit as planet candidate or false positive.',
      built: 'AstroNetModel (5-block global + 2-block local branch) + AdvancedAstroNetModel with MultiHeadAttention (ExoMiner-inspired).',
      source: 'AstroNet (Shallue 2018), ExoMiner (Valizadegan 2022) — architecture rebuilt from scratch.',
    },
    {
      num: 5, name: 'Vetting', icon: '🔍',
      what: 'Three automated tests flag likely false positives.',
      built: 'SNR calculation, odd-even transit depth comparison, secondary eclipse search at phase 0.5.',
      source: 'Standard TCE vetting criteria (Jenkins et al. 2010)',
    },
    {
      num: 6, name: 'Transit Fitting', icon: '📈',
      what: 'PyTransit RoadRunner model fits the transit shape to extract physical parameters.',
      built: 'Nelder-Mead optimization on folded local view. Extracts k (Rp/Rs), a/Rs, inclination.',
      source: 'PyTransit (Parviainen 2015)',
    },
  ];

  return (
    <div className="space-y-12">
      <header className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">About ExoAstro</h1>
        <p className="text-slate-400 max-w-2xl">
          An end-to-end machine learning pipeline for detecting exoplanet candidates in Kepler photometric data.
          Every component is purpose-built for this platform.
        </p>
      </header>

      {/* Architecture */}
      <section>
        <h2 className="text-xl font-bold text-slate-200 mb-6">Pipeline Architecture</h2>
        <div className="space-y-4">
          {pipelineStages.map((stage) => (
            <div key={stage.num} className="glass rounded-2xl p-6 flex gap-5">
              <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-indigo-900/30 border border-indigo-700/30 flex items-center justify-center text-2xl">
                {stage.icon}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-xs text-slate-600 font-mono">Step {stage.num}</span>
                  <h3 className="font-bold text-slate-200">{stage.name}</h3>
                </div>
                <p className="text-sm text-slate-400 mb-3">{stage.what}</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                  <div className="bg-slate-900/50 rounded-lg px-3 py-2">
                    <span className="text-indigo-400 font-semibold">Built: </span>
                    <span className="text-slate-400">{stage.built}</span>
                  </div>
                  <div className="bg-slate-900/50 rounded-lg px-3 py-2">
                    <span className="text-violet-400 font-semibold">Sources: </span>
                    <span className="text-slate-400">{stage.source}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Tech Stack */}
      <section className="glass rounded-2xl p-8">
        <h2 className="text-xl font-bold text-slate-200 mb-4">Tech Stack</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {[
            { name: 'Lightkurve', role: 'Light curve fetch + BLS', type: 'Python' },
            { name: 'TensorFlow / Keras', role: 'CNN + Attention model', type: 'Python' },
            { name: 'PyTransit', role: 'Transit model fitting', type: 'Python' },
            { name: 'SciPy', role: 'Nelder-Mead optimizer', type: 'Python' },
            { name: 'NumPy / Matplotlib', role: 'Data processing + plots', type: 'Python' },
            { name: 'Next.js 16 + React 19', role: 'Dashboard frontend', type: 'TypeScript' },
          ].map((tech) => (
            <div key={tech.name} className="bg-slate-900/50 rounded-xl p-4 border border-slate-800/50">
              <div className="text-sm font-semibold text-slate-200">{tech.name}</div>
              <div className="text-xs text-slate-500 mt-1">{tech.role}</div>
              <div className="text-xs text-indigo-400 mt-2 font-mono">{tech.type}</div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
