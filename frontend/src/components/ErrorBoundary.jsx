import React from 'react';

// ─── ErrorBoundary ─────────────────────────────────────────────────────────────
/**
 * Catches any render error in its children and shows a friendly fallback UI.
 *
 * Props:
 *   children      – the component tree to protect
 *   fallback      – optional custom ReactNode to render on error
 *   onError       – optional (error, info) => void callback (e.g. send to Sentry)
 *   resetOnNavKey – optional string — when this prop changes (e.g. pathname),
 *                   the boundary resets automatically (good for route changes)
 *
 * Usage:
 *   <ErrorBoundary>
 *     <ListPage />
 *   </ErrorBoundary>
 *
 *   <ErrorBoundary fallback={<p>Custom error</p>} onError={logToSentry}>
 *     <AnalyticsPage />
 *   </ErrorBoundary>
 */
export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, eventId: null };
    this.handleReset = this.handleReset.bind(this);
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    // Call optional external logger (e.g. Sentry)
    if (typeof this.props.onError === 'function') {
      this.props.onError(error, info);
    }
    // Dev-mode console output
    if (import.meta.env.DEV) {
      console.error('[ErrorBoundary] Caught error:', error, info.componentStack);
    }
  }

  // Reset when a navigation key changes (e.g. React Router pathname)
  componentDidUpdate(prevProps) {
    if (
      this.state.hasError &&
      this.props.resetOnNavKey !== undefined &&
      this.props.resetOnNavKey !== prevProps.resetOnNavKey
    ) {
      this.handleReset();
    }
  }

  handleReset() {
    this.setState({ hasError: false, error: null });
  }

  render() {
    if (this.state.hasError) {
      // Custom fallback provided by parent
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // Default fallback UI
      return <ErrorFallback error={this.state.error} onReset={this.handleReset} />;
    }

    return this.props.children;
  }
}

// ─── Default fallback UI ───────────────────────────────────────────────────────
function ErrorFallback({ error, onReset }) {
  const isDev  = import.meta.env.DEV;
  const msg    = error?.message ?? 'An unexpected error occurred.';

  return (
    <div
      role="alert"
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        padding: '3rem 2rem',
        animation: 'eb-fadein 0.3s ease both',
      }}
    >
      {/* Icon */}
      <svg width="56" height="56" viewBox="0 0 56 56" fill="none" aria-hidden="true" style={{ marginBottom: 16 }}>
        <circle cx="28" cy="28" r="28" fill="#FEF0F0" />
        <path d="M28 18 L28 32" stroke="#E24B4A" strokeWidth="2.5" strokeLinecap="round" />
        <circle cx="28" cy="39" r="2" fill="#E24B4A" />
      </svg>

      <h2 style={{
        margin: '0 0 8px',
        fontSize: 17,
        fontWeight: 500,
        color: 'var(--color-text-primary)',
      }}>
        Something went wrong
      </h2>

      <p style={{
        margin: '0 0 20px',
        fontSize: 13,
        color: 'var(--color-text-secondary)',
        maxWidth: 320,
        lineHeight: 1.6,
      }}>
        This section encountered an error and couldn't render. Your data is safe.
      </p>

      {/* Dev-only stack trace */}
      {isDev && (
        <details style={{
          marginBottom: 20,
          maxWidth: 480,
          width: '100%',
          textAlign: 'left',
          background: 'var(--color-background-secondary)',
          border: '0.5px solid var(--color-border-secondary)',
          borderRadius: 8,
          padding: '8px 12px',
        }}>
          <summary style={{ fontSize: 12, fontWeight: 500, cursor: 'pointer', color: '#E24B4A' }}>
            Error details (dev only)
          </summary>
          <pre style={{
            marginTop: 8, fontSize: 11,
            color: 'var(--color-text-secondary)',
            whiteSpace: 'pre-wrap', wordBreak: 'break-word',
          }}>
            {msg}
          </pre>
        </details>
      )}

      <div style={{ display: 'flex', gap: 10 }}>
        <button
          onClick={onReset}
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
          }}
        >
          Try again
        </button>
        <button
          onClick={() => window.location.reload()}
          style={{
            padding: '8px 20px',
            fontSize: 13,
            background: 'transparent',
            color: 'var(--color-text-secondary)',
            border: '0.5px solid var(--color-border-secondary)',
            borderRadius: 8,
            cursor: 'pointer',
            minHeight: 44,
          }}
        >
          Reload page
        </button>
      </div>

      <style>{`
        @keyframes eb-fadein {
          from { opacity: 0; transform: scale(0.97); }
          to   { opacity: 1; transform: scale(1); }
        }
      `}</style>
    </div>
  );
}

export default ErrorBoundary;
