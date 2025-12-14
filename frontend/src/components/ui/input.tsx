export function Input({ className="", ...props }: any) {
  return (
    <input
      {...props}
      className={`border border-neutral-700 bg-neutral-900 rounded px-3 py-2 ${className}`}
    />
  );
}
