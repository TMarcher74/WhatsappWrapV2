import { useState } from "react";
import slides from "./slides";

export default function WrappedPage({ analysis }) {
  const [current, setCurrent] = useState(0);

  const CurrentSlide = slides[current];

  return (
    <div className="min-h-screen bg-black text-white">
      <CurrentSlide data={analysis} next={() => setCurrent(current + 1)} />
    </div>
  );
}
