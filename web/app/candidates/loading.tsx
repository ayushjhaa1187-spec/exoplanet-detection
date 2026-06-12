export default function Loading() {
  return (
    <div className="space-y-8 py-4">
      <header className="space-y-2">
        <div className="h-9 w-64 skeleton rounded-md" />
        <div className="h-5 w-96 skeleton rounded-md" />
      </header>

      {/* Info banner skeleton */}
      <div className="h-16 w-full skeleton rounded-xl" />

      {/* Table skeleton */}
      <div className="card overflow-hidden">
        <div className="w-full">
          <div className="border-b border-border-subtle bg-surface-alt/80 flex px-6 py-4">
            <div className="flex-1 h-4 skeleton rounded" />
            <div className="flex-1 h-4 skeleton rounded mx-4" />
            <div className="flex-1 h-4 skeleton rounded mx-4" />
            <div className="flex-1 h-4 skeleton rounded" />
          </div>
          <div className="divide-y divide-border-subtle">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="flex px-6 py-5 table-row-alt">
                <div className="flex-1">
                  <div className="h-5 w-32 skeleton rounded mb-2" />
                  <div className="h-3 w-20 skeleton rounded" />
                </div>
                <div className="flex-1 flex items-center px-4">
                  <div className="h-6 w-24 skeleton rounded-full" />
                </div>
                <div className="flex-1 flex items-center px-4">
                  <div className="h-3 w-full max-w-[120px] skeleton rounded-full" />
                </div>
                <div className="flex-1 flex items-center justify-end">
                  <div className="h-4 w-16 skeleton rounded" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
