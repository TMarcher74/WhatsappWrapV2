import React, { useEffect, useState } from "react";

export default function SlideNumber({ slides }) {
  const [current, setCurrent] = useState(1);

  useEffect(() => {
    const handler = () => {
      const sections = [...document.querySelectorAll("section")];

      sections.forEach((sec, i) => {
        const rect = sec.getBoundingClientRect();
        if (rect.top <= window.innerHeight * 0.5 && rect.bottom >= window.innerHeight * 0.5) {
          setCurrent(i + 1);
        }
      });
    };

    window.addEventListener("scroll", handler);
    return () => window.removeEventListener("scroll", handler);
  }, []);

  return (
    <div className="fixed right-6 top-1/2 -translate-y-1/2 text-white text-xl opacity-80">
      {current} / {slides}
    </div>
  );
}
