import Link from 'next/link';

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col">
      <div className="p-6">
        <h1 className="text-xl font-bold text-indigo-400">ExoAstro</h1>
        <p className="text-xs text-slate-400 mt-1">Detection Platform</p>
      </div>
      <nav className="flex-1 px-4 space-y-2">
        <Link href="/" className="block px-4 py-2 rounded text-slate-300 hover:bg-slate-800 hover:text-white transition">Dashboard</Link>
        <Link href="/candidates" className="block px-4 py-2 rounded text-slate-300 hover:bg-slate-800 hover:text-white transition">Candidates</Link>
        <Link href="/metrics" className="block px-4 py-2 rounded text-slate-300 hover:bg-slate-800 hover:text-white transition">Metrics</Link>
        <Link href="/reports" className="block px-4 py-2 rounded text-slate-300 hover:bg-slate-800 hover:text-white transition">Reports</Link>
        <Link href="/about" className="block px-4 py-2 rounded text-slate-300 hover:bg-slate-800 hover:text-white transition">About</Link>
      </nav>
      <div className="p-4 border-t border-slate-800 text-xs text-slate-500">
        v1.0.0-beta
      </div>
    </aside>
  );
}
