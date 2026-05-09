import React from 'react';

// ─── SVG illustrations — inline, zero dependencies ────────────────────────────

const illustrations = {
  noData: (
    <svg width="120" height="100" viewBox="0 0 120 100" fill="none" aria-hidden="true">
      <rect x="18" y="28" width="84" height="56" rx="6" fill="#EDF0F7" />
      <rect x="18" y="28" width="84" height="14" rx="6" fill="#D1D8E8" />
      <rect x="28" y="52" width="40" height="6" rx="3" fill="#C5CEDF" />
      <rect x="28" y="64" width="28" height="6" rx="3" fill="#D1D8E8" />
      <circle cx="88" cy="32" r="2" fill="#A0AABF" />
      <circle cx="94" cy="32" r="2" fill="#A0AABF" />
      <circle cx="100" cy="32" r="2" fill="#A0AABF" />
      {/* Magnifying glass */}
      <circle cx="62" cy="42" r="14" stroke="#A0AABF" strokeWidth="2.5" fill="white" opacity="0.7" />
      <line x1="72" y1="52" x2="80" y2="60" stroke="#A0AABF" strokeWidth="2.5" strokeLinecap="round" />
      <line x1="56" y1="42" x2="66" y2="42" stroke="#C5CEDF" strokeWidth="2" strokeLinecap="round" />
      <line x1="61" y1="37" x2="61" y2="47" stroke="#C5CEDF" strokeWidth="2" strokeLinecap="round" />
    </svg>
  ),

  noResults: (
    <svg width="120" height="100" viewBox="0 0 120 100" fill="none" aria-hidden="true">
      <circle cx="60" cy="46" r="28" fill="#EDF0F7" />
      <circle cx="60" cy="46" r="20" fill="white" />
      {/* X mark */}
      <line x1="53" y1="39" x2="67" y2="53" stroke="#C5CEDF" strokeWidth="3" strokeLinecap="round" />
      <line x1="67" y1="39" x2="53" y2="53" stroke="#C5CEDF" strokeWidth="3" strokeLinecap="round" />
      {/* Filter lines */}
      <rect x="22" y="18" width="76" height="6" rx="3" fill="#D1D8E8" />
      <rect x="32" y="18" width="56" height="6" rx="3" fill="#1B4F8A" opacity="0.2" />
      <rect x="30" y="80" width="60" height="6" rx="3" fill="#EDF0F7" />
    </svg>
  ),

  noActivity: (
    <svg width="120" height="100" viewBox="0 0 120 100" fill="none" aria-hidden="true">
      {/* Calendar */}
      <rect x="22" y="22" width="76" height="62" rx="8" fill="#EDF0F7" />
      <rect x="22" y="22" width="76" height="22" rx="8" fill="#D1D8E8" />
      <rect x="22" y="34" width="76" height="10" fill="#D1D8E8" />
      {/* Dot grid */}
      {[0,1,2,3].map(col => [0,1,2].map(row => (
        <circle
          key={`${col}-${row}`}
          cx={36 + col * 17}
          cy={60 + row * 13}
          r="3"
          fill={col === 1 && row === 1 ? '#1B4F8A' : '#C5CEDF'}
          opacity={col === 1 && row === 1 ? 0.5 : 1}
        />
      )))}
      {/* Binding holes */}
      <circle cx="42" cy="22" r="4" fill="white" />
      <circle cx="78" cy="22" r="4" fill="white" />
    </svg>
  ),

  noFiles: (
    <svg width="120" height="100" viewBox="0 0 120 100" fill="none" aria-hidden="true">
      <rect x="30" y="16" width="52" height="68" rx="6" fill="#EDF0F7" />
      <path d="M68 16 L82 30 L68 30 Z" fill="#D1D8E8" />
      <rect x="68" y="16" width="14" height="14" rx="2" fill="#D1D8E8" />
      <rect x="40" y="42" width="32" height="4" rx="2" fill="#C5CEDF" />
      <rect x="40" y="52" width="24" height="4" rx="2" fill="#D1D8E8" />
      <rect x="40" y="62" width="28" height="4" rx="2" fill="#C5CEDF" />
      {/* Upload arrow */}
      <circle cx="60" cy="84" r="10" fill="#1B4F8A" opacity="0.12" />
      <path d="M60 80 L60 88 M57 83 L60 80 L63 83" stroke="#1B4F8A" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" opacity="0.6" />
    </svg>
  ),

  error: (
    <svg width="120" height="100" viewBox="0 0 120 100" fill="none" aria-hidden="true">
      <circle cx="60" cy="50" r="30" fill="#FEF0F0" />
      <circle cx="60" cy="50" r="22" fill="white" />
      <path d="M60 36 L60 54" stroke="#E24B4A" strokeWidth="3" strokeLinecap="round" />
      <circle cx="60" cy="62" r="2.5" fill="#E24B4A" />
      {/* Dashes around circle */}
      {[0,45,90,135,180,225,270,315].map((deg, i) => {
        const r = 28;
        const rad = (deg * Math.PI) / 180;
        const x1 = 60 + r * Math.cos(rad);
        const y1 = 50 + r * Math.sin(rad);
        const x2 = 60 + (r + 5) * Math.cos(rad);
        const y2 = 50 + (r + 5) * Math.sin(rad);
        return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#FBCACA" strokeWidth="2" strokeLinecap="round" />;
      })}
    </svg>
  ),
};

// ─── Config map ───────────────────────────────────────────────────────────────
const presets = {
  'no-data': {
    illustration: 'noData',
    heading: 'Nothing here yet',
    body: 'Create your first record to get started.',
  },
  'no-results': {
    illustration: 'noResults',
    heading: 'No results found',
    body: 'Try adjusting your search or filter criteria.',
  },
  'no-activity': {
    illustration: 'noActivity',
    heading: 'No recent activity',
    body: 'Actions taken on records will appear here.',
  },
  'no-files': {
    illustration: 'noFiles',
    heading: 'No files attached',
    body: 'Upload a file to attach it to this record.',
  },
  'error': {
    illustration: 'error',
    heading: 'Something went wrong',
    body: 'An unexpected error occurred. Please try again.',
  },
};

// ─── EmptyState component ─────────────────────────────────────────────────────
/**
 * Props:
 *   variant   – 'no-data' | 'no-results' | 'no-activity' | 'no-files' | 'error'
 *   heading   – override the default heading text
 *   body      – override the default body text
 *   action    – { label: string, onClick: fn } — renders a primary button
 *   compact   – boolean — smaller padding for inline use
 */
export default function EmptyState({
  variant = 'no-data',
  heading,
  body,
  action,
  compact = false,
}) {
  const preset = presets[variant] ?? presets['no-data'];
  const illustrationKey = preset.illustration;

  return (
    <div
      role="status"
      aria-live="polite"
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        padding: compact ? '2rem 1rem' : '4rem 2rem',
        gap: 0,
        animation: 'es-fadein 0.35s ease both',
      }}
    >
      {/* Illustration */}
      <div style={{ marginBottom: compact ? 12 : 20, opacity: 0.9 }}>
        {illustrations[illustrationKey]}
      </div>

      {/* Heading */}
      <h3 style={{
        margin: '0 0 6px',
        fontSize: compact ? 14 : 16,
        fontWeight: 500,
        color: 'var(--color-text-primary)',
        letterSpacing: '-0.01em',
      }}>
        {heading ?? preset.heading}
      </h3>

      {/* Body text */}
      <p style={{
        margin: '0 0 ' + (action ? '20px' : '0'),
        fontSize: compact ? 12 : 13,
        color: 'var(--color-text-secondary)',
        lineHeight: 1.6,
        maxWidth: 280,
      }}>
        {body ?? preset.body}
      </p>

      {/* Optional action button */}
      {action && (
        <button
          onClick={action.onClick}
          style={{
            padding: '8px 20px',
            fontSize: 13,
            fontWeight: 500,
            background: '#1B4F8A',
            color: '#fff',
            border: 'none',
            borderRadius: 8,
            cursor: 'pointer',
            minHeight: 44,
            transition: 'opacity 0.15s',
          }}
          onMouseOver={e => { e.currentTarget.style.opacity = '0.88'; }}
          onMouseOut={e =>  { e.currentTarget.style.opacity = '1'; }}
        >
          {action.label}
        </button>
      )}

      <style>{`
        @keyframes es-fadein {
          from { opacity: 0; transform: translateY(8px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
}
