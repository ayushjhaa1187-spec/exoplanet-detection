export default function StatsCard({ title, value, description }: { title: string, value: string | number, description: string }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm">
      <h3 className="text-sm font-medium text-slate-400">{title}</h3>
      <p className="text-3xl font-bold text-white mt-2">{value}</p>
      <p className="text-xs text-slate-500 mt-1">{description}</p>
    </div>
  );
}
