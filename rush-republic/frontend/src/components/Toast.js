import React, { useEffect, useState } from 'react';
import './Toast.css';

export default function Toast({ message, show, duration = 2600, onDone }) {
  const [leaving, setLeaving] = useState(false);

  useEffect(() => {
    if (!show) return undefined;

    setLeaving(false);
    const leaveTimer = setTimeout(() => setLeaving(true), duration - 300);
    const doneTimer = setTimeout(() => {
      if (onDone) onDone();
    }, duration);

    return () => {
      clearTimeout(leaveTimer);
      clearTimeout(doneTimer);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [show, duration]);

  if (!show) return null;

  return (
    <div className="rr-toast-layer" role="status" aria-live="polite">
      <div className={`rr-toast${leaving ? ' rr-toast--leaving' : ''}`}>
        <span className="rr-toast__icon" aria-hidden="true">
          <svg viewBox="0 0 20 20" width="16" height="16">
            <path
              d="M4 10.5L8 14.5L16 5.5"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </span>
        <span className="rr-toast__message">{message}</span>
      </div>
    </div>
  );
}