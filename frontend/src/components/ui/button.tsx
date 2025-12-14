import * as React from "react";

export function Button({ children, className="", ...props }: any) {
  return (
    <button
      {...props}
      className={`px-4 py-2 rounded bg-neutral-700 hover:bg-neutral-600 transition ${className}`}
    >
      {children}
    </button>
  );
}
ss