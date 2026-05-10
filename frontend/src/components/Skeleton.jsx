import React from 'react';

// ─── Base shimmer block ───────────────────────────────────────────────────────
const Shimmer = ({ width = '100%', height = 16, radius = 6, style = {} }) => (
  <div
    aria-hidden="true"
    style={{
      width,
      height,
      borderRadius: radius,
      background: 'linear-gradient(90deg, var(--sk-base) 25%, var(--sk-shine) 50%, var(--sk-base) 75%)',
      backgroundSize: '200% 100%',
      animation: 'sk-shimmer 1.6s ease-in-out infinite',
      ...style,
    }}
  />
);

// ─── Global keyframe injected once ───────────────────────────────────────────
const STYLES = `
  :root {
    --sk-base:  #e8eaed;
    --sk-shine: #f4f5f7;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --sk-base:  #2a2d31;
      --sk-shine: #33373d;
    }
  }
  @keyframes sk-shimmer {
    0%   { background-position: 200% 0; }
    100% { background-position: -200% 0; }
  }
`;

function InjectStyles() {
  if (typeof document !== 'undefined' && !document.getElementById('sk-styles')) {
    const tag = document.createElement('style');
    tag.id = 'sk-styles';
    tag.textContent = STYLES;
    document.head.appendChild(tag);
  }
  return null;
}

// ─── Table skeleton (list page) ───────────────────────────────────────────────
export function TableSkeleton({ rows = 6, cols = 5 }) {
  InjectStyles();
  return (
    <div role="status" aria-label="Loading table…" style={{ width: '100%' }}>
      {/* Header row */}
      <div style={rowStyle('var(--sk-base)', true)}>
        {Array.from({ length: cols }).map((_, i) => (
          <Shimmer key={i} width={i === 0 ? '40%' : '60%'} height={12} />
        ))}
      </div>

      {/* Data rows */}
      {Array.from({ length: rows }).map((_, r) => (
        <div
          key={r}
          style={{
            ...rowStyle(),
            animationDelay: `${r * 60}ms`,
            opacity: 1 - r * 0.08,
          }}
        >
          {Array.from({ length: cols }).map((_, c) => (
            <Shimmer
              key={c}
              width={c === 0 ? '55%' : c === cols - 1 ? '30%' : '70%'}
              height={14}
              style={{ animationDelay: `${(r * cols + c) * 30}ms` }}
            />
          ))}
        </div>
      ))}
      <span className="sr-only">Loading…</span>
    </div>
  );
}

// ─── Card grid skeleton (dashboard KPI cards) ─────────────────────────────────
export function CardGridSkeleton({ cards = 4 }) {
  InjectStyles();
  return (
    <div
      role="status"
      aria-label="Loading cards…"
      style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}
    >
      {Array.from({ length: cards }).map((_, i) => (
        <div
          key={i}
          style={{
            flex: '1 1 160px',
            padding: '1rem',
            borderRadius: 10,
            background: 'var(--sk-base)',
            display: 'flex',
            flexDirection: 'column',
            gap: 10,
          }}
        >
          <Shimmer width="50%" height={11} style={{ animationDelay: `${i * 80}ms` }} />
          <Shimmer width="35%" height={28} radius={4} style={{ animationDelay: `${i * 80 + 40}ms` }} />
          <Shimmer width="65%" height={10} style={{ animationDelay: `${i * 80 + 80}ms` }} />
        </div>
      ))}
      <span className="sr-only">Loading…</span>
    </div>
  );
}

// ─── Detail page skeleton ─────────────────────────────────────────────────────
export function DetailSkeleton() {
  InjectStyles();
  return (
    <div role="status" aria-label="Loading record…" style={{ maxWidth: 720, padding: '1.5rem 0' }}>
      {/* Title + badge */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 24 }}>
        <Shimmer width="45%" height={26} radius={6} />
        <Shimmer width={64} height={22} radius={999} />
      </div>

      {/* Field rows */}
      {[['30%', '55%'], ['25%', '70%'], ['35%', '48%'], ['28%', '62%'], ['20%', '75%']].map(
        ([lw, vw], i) => (
          <div key={i} style={{ display: 'flex', gap: 16, marginBottom: 16, alignItems: 'center' }}>
            <Shimmer width={lw} height={12} style={{ animationDelay: `${i * 60}ms` }} />
            <Shimmer width={vw} height={14} style={{ animationDelay: `${i * 60 + 30}ms` }} />
          </div>
        )
      )}

      {/* AI analysis card */}
      <div style={{ marginTop: 28, padding: 16, borderRadius: 10, background: 'var(--sk-base)' }}>
        <Shimmer width="30%" height={13} style={{ marginBottom: 12 }} />
        <Shimmer width="100%" height={11} style={{ marginBottom: 8, animationDelay: '80ms' }} />
        <Shimmer width="90%"  height={11} style={{ marginBottom: 8, animationDelay: '120ms' }} />
        <Shimmer width="75%"  height={11} style={{ animationDelay: '160ms' }} />
      </div>

      <span className="sr-only">Loading…</span>
    </div>
  );
}

// ─── Form skeleton ────────────────────────────────────────────────────────────
export function FormSkeleton({ fields = 5 }) {
  InjectStyles();
  return (
    <div role="status" aria-label="Loading form…" style={{ maxWidth: 560 }}>
      <Shimmer width="40%" height={22} radius={6} style={{ marginBottom: 28 }} />
      {Array.from({ length: fields }).map((_, i) => (
        <div key={i} style={{ marginBottom: 20 }}>
          <Shimmer width="28%" height={11} style={{ marginBottom: 8, animationDelay: `${i * 70}ms` }} />
          <Shimmer width="100%" height={40} radius={8} style={{ animationDelay: `${i * 70 + 35}ms` }} />
        </div>
      ))}
      {/* Submit button */}
      <Shimmer width={120} height={40} radius={8} style={{ marginTop: 12 }} />
      <span className="sr-only">Loading…</span>
    </div>
  );
}

// ─── Chart skeleton (analytics page) ─────────────────────────────────────────
export function ChartSkeleton({ height = 260, label = 'Loading chart…' }) {
  InjectStyles();
  const bars = [55, 80, 45, 90, 65, 70, 50, 85, 60, 75];
  return (
    <div
      role="status"
      aria-label={label}
      style={{
        height,
        padding: '16px',
        borderRadius: 12,
        background: 'var(--color-background-primary, #fff)',
        border: '0.5px solid var(--sk-base)',
        display: 'flex',
        alignItems: 'flex-end',
        gap: 8,
        overflow: 'hidden',
      }}
    >
      {bars.map((pct, i) => (
        <div
          key={i}
          style={{
            flex: 1,
            height: `${pct}%`,
            borderRadius: '4px 4px 0 0',
            background: 'linear-gradient(90deg, var(--sk-base) 25%, var(--sk-shine) 50%, var(--sk-base) 75%)',
            backgroundSize: '200% 100%',
            animation: `sk-shimmer 1.6s ease-in-out infinite`,
            animationDelay: `${i * 100}ms`,
          }}
        />
      ))}
      <span className="sr-only">{label}</span>
    </div>
  );
}

// ─── Row style helper ─────────────────────────────────────────────────────────
function rowStyle(bg, isHeader = false) {
  return {
    display: 'grid',
    gridTemplateColumns: 'repeat(5, 1fr)',
    gap: 12,
    padding: '12px 16px',
    background: bg ?? 'transparent',
    borderBottom: '1px solid var(--sk-base)',
    alignItems: 'center',
    ...(isHeader ? { borderRadius: '8px 8px 0 0', paddingBottom: 14 } : {}),
  };
}

// ─── Named export for the simplest use-case: inline text line ────────────────
export function LineSkeleton({ width = '80%', height = 14 }) {
  InjectStyles();
  return <Shimmer width={width} height={height} />;
}

export default {
  Table:    TableSkeleton,
  CardGrid: CardGridSkeleton,
  Detail:   DetailSkeleton,
  Form:     FormSkeleton,
  Chart:    ChartSkeleton,
  Line:     LineSkeleton,
};
