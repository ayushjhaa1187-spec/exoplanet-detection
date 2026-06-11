export default function PipelineFlow() {
  const steps = [
    { name: "Fetch Data", desc: "Lightkurve MAST integration" },
    { name: "Preprocess", desc: "Global/Local Binning" },
    { name: "Classify", desc: "Advanced AstroNet CNN" },
    { name: "Vet", desc: "SNR & Odd-Even Analysis" },
    { name: "Fit Transit", desc: "PyTransit Modeling" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <h3 className="text-lg font-bold mb-6">Pipeline Flow</h3>
      <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
        {steps.map((step, idx) => (
          <div key={idx} className="flex-1 flex flex-col items-center text-center w-full">
            <div className="w-12 h-12 rounded-full bg-indigo-900/50 border border-indigo-500 flex items-center justify-center text-indigo-400 font-bold mb-3 z-10 relative">
              {idx + 1}
            </div>
            <h4 className="font-medium text-sm text-slate-200">{step.name}</h4>
            <p className="text-xs text-slate-500 mt-1">{step.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
