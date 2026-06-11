export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-12">
      <header>
        <h1 className="text-3xl font-bold">About the Architecture</h1>
        <p className="text-slate-400 mt-2">Design decisions and project lineage.</p>
      </header>

      <section className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-xl font-bold text-white">Project Lineage & Borrowed Components</h2>
        <p className="text-sm text-slate-300 leading-relaxed">
          This platform was constructed over a structured 15-day build. Rather than reinventing the wheel, 
          it strategically integrates best-in-class approaches from top exoplanet research repositories while 
          maintaining a clean, independent source architecture.
        </p>
        
        <ul className="list-disc pl-5 text-sm text-slate-300 space-y-2 mt-4">
          <li><strong>Lightkurve</strong>: Used for reliable MAST API interactions, data stitching, and BLS periodogram implementation.</li>
          <li><strong>AstroNet (exoplanet-ml)</strong>: Borrowed the Global/Local binning paradigm and base 1D CNN architecture.</li>
          <li><strong>ExoMiner</strong>: Inspired the transition to an Advanced AstroNet model incorporating Multi-Head Attention blocks.</li>
          <li><strong>LATTE</strong>: Guided the vetting strategy (Odd-Even mismatch checks, SNR diagnostics) to prune false positives.</li>
          <li><strong>PyTransit</strong>: Utilized the RoadRunner analytical transit model for deep scientific parameter fitting.</li>
        </ul>
      </section>

      <section className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-xl font-bold text-white">What Was Built</h2>
        <p className="text-sm text-slate-300 leading-relaxed">
          The core innovation of this project lies in <strong>integration and presentation</strong>. 
          The disparate scripts and workflows of the reference repositories were completely refactored into a 
          cohesive, modular Python pipeline (`src/`). Furthermore, this Next.js + TypeScript dashboard was built 
          from scratch to provide a seamless, presentation-ready product layer, transforming raw scientific logs 
          into an interpretable, interactive story.
        </p>
      </section>
    </div>
  );
}
