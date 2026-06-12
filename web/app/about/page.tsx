export default function AboutPage() {
  const pipelineStages = [
    {
      num: 1, name: 'Fetch', icon: '📡',
      what: 'Light curves are fetched from NASA MAST using the Lightkurve library, followed by a Box Least Squares (BLS) period search to locate periodic transit signals.',
      built: 'Custom ExoplanetDataFetcher wrapper + BLS search grid from 0.5 to 400 days.',
      source: 'Lightkurve, MAST (public archive), Kovács et al. (2002)',
    },
    {
      num: 2, name: 'Preprocess', icon: '⚙️',
      what: 'The light curve is phase-folded and binned into global (2001 bins) and local (201 bins) views.',
      built: 'Custom ExoplanetPreprocessor with median-aggregation binning and data augmentation.',
      source: 'AstroNet paper (Shallue & Vanderburg 2018)',
    },
    {
      num: 3, name: 'CNN', icon: '🧠',
      what: 'A dual-branch 1D convolutional neural network with Multi-Head Attention blocks classifies the transit signature.',
      built: 'AdvancedAstroNetModel (global/local branches + ExoMiner-inspired attention layers).',
      source: 'AstroNet (Shallue 2018), ExoMiner (Valizadegan 2022)',
    },
    {
      num: 4, name: 'Vet', icon: '🔍',
      what: 'Automated diagnostic tests are run to filter out false positive signals.',
      built: 'SNR checks, odd-even transit depth consistency, and secondary eclipse depth testing.',
      source: 'Standard Kepler TCE Vetting (Jenkins et al. 2010)',
    },
    {
      num: 5, name: 'Fit', icon: '📈',
      what: 'A scientific transit model fits the light curve shape to estimate planetary parameters.',
      built: 'Nelder-Mead optimization using PyTransit RoadRunner to extract radius ratio k (Rp/Rs).',
      source: 'PyTransit (Parviainen 2015)',
    },
  ];

  return (
    <div className="space-y-12 py-4">
      <header className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight text-text-primary">About ExoAstro</h1>
        <p className="text-text-secondary max-w-2xl text-lg">
          An end-to-end machine learning pipeline for detecting exoplanet candidates in Kepler photometric data.
          Every component is purpose-built for this platform.
        </p>
      </header>

      {/* Architecture */}
      <section>
        <h2 className="text-xl font-bold text-text-primary mb-6">Pipeline Architecture</h2>
        <div className="space-y-4 relative">
          <div className="absolute left-6 top-8 bottom-8 w-px bg-border-subtle hidden md:block"></div>
          {pipelineStages.map((stage) => (
            <div key={stage.num} className="card p-6 flex gap-6 relative z-10 hover:border-brand-primary/30 transition-colors">
              <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-surface-alt border border-border-subtle flex items-center justify-center text-2xl shadow-sm">
                {stage.icon}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-xs text-brand-secondary font-mono bg-brand-secondary/10 px-2 py-0.5 rounded font-bold">Step {stage.num}</span>
                  <h3 className="font-bold text-text-primary text-lg">{stage.name}</h3>
                </div>
                <p className="text-sm text-text-secondary mb-4">{stage.what}</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                  <div className="bg-surface-alt rounded-lg px-4 py-3 border border-border-subtle">
                    <span className="text-brand-primary font-semibold block mb-1 uppercase tracking-wider text-[10px]">Built</span>
                    <span className="text-text-secondary">{stage.built}</span>
                  </div>
                  <div className="bg-surface-alt rounded-lg px-4 py-3 border border-border-subtle">
                    <span className="text-brand-secondary font-semibold block mb-1 uppercase tracking-wider text-[10px]">Sources</span>
                    <span className="text-text-secondary">{stage.source}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Tech Stack */}
      <section className="card p-8 bg-gradient-to-br from-surface-card to-surface-alt/50 border-t-4 border-t-brand-primary">
        <h2 className="text-xl font-bold text-text-primary mb-6">Tech Stack</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {[
            { name: 'Lightkurve', role: 'Light curve fetch + BLS', type: 'Python' },
            { name: 'TensorFlow / Keras', role: 'CNN + Attention model', type: 'Python' },
            { name: 'PyTransit', role: 'Transit model fitting', type: 'Python' },
            { name: 'SciPy', role: 'Nelder-Mead optimizer', type: 'Python' },
            { name: 'NumPy / Matplotlib', role: 'Data processing + plots', type: 'Python' },
            { name: 'Next.js 16 + React 19', role: 'Dashboard frontend', type: 'TypeScript' },
          ].map((tech) => (
            <div key={tech.name} className="bg-surface-card rounded-xl p-5 border border-border-subtle shadow-sm hover:shadow-md transition-shadow">
              <div className="text-sm font-semibold text-text-primary">{tech.name}</div>
              <div className="text-xs text-text-secondary mt-1">{tech.role}</div>
              <div className="text-xs text-brand-primary mt-3 font-mono font-medium">{tech.type}</div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
