import React, { useState, useEffect } from "react";

export default function TypingHeader({ text, speed = 50 }) {
  const [display, setDisplay] = useState("");

  useEffect(() => {
    let i = 0;
    const interval = setInterval(() => {
      setDisplay(text.slice(0, i));
      i++;
      if (i > text.length) clearInterval(interval);
    }, speed);

    return () => clearInterval(interval);
  }, [text]);

  return (
    <h1 className="text-4xl font-bold text-wa-green mb-6">
      {display}
      <span className="animate-pulse">▌</span>
    </h1>
  );
}
