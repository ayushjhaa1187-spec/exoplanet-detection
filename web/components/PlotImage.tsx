'use client';

const FALLBACK = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(
  `<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="#0f1629"/>
    <text x="50%" y="45%" fill="#475179" text-anchor="middle" dy=".3em" font-size="14" font-family="monospace">Plot pending pipeline run</text>
    <text x="50%" y="58%" fill="#334155" text-anchor="middle" dy=".3em" font-size="11" font-family="monospace">Run the pipeline to generate this plot</text>
  </svg>`
)}`;

export default function PlotImage({
  src,
  alt,
  className,
}: {
  src: string;
  alt: string;
  className?: string;
}) {
  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={src}
      alt={alt}
      className={className ?? 'w-full h-full object-cover'}
      onError={(e) => {
        (e.target as HTMLImageElement).src = FALLBACK;
      }}
    />
  );
}
