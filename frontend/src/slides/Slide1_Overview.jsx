import React from "react";
import TypingHeader from "../components/TypingHeader";
import FadeIn from "../components/FadeIn";

export default function Slide1_Overview({ data }) {
  if (!data) return null;

  const users = data.users || [];
const totalMessages = Object.values(data.total_messages || {})
  .reduce((a, b) => a + b, 0);

const totalWords = Object.values(data.word_character_stats || {})
  .reduce((a, b) => a + (b?.words || 0), 0);

const totalChars = Object.values(data.word_character_stats || {})
  .reduce((a, b) => a + (b?.characters || 0), 0);


  const activeDays = Object.keys(data.date_frequency || {}).length;

  return (
  <div className="h-full w-full flex flex-col justify-center items-center text-center text-white px-10">

    {/* ACT I — TITLE */}
    <TypingHeader text="This Wasn’t Just a Chat." />

    {/* ACT II — STORY SENTENCE */}
    <FadeIn delay={0.6}>
      <p className="text-3xl md:text-4xl font-light text-gray-200 max-w-5xl leading-relaxed mt-8">
        It was a conversation that lasted{" "}
        <span className="font-semibold text-white">{activeDays}</span>{" "}
        days, exchanged{" "}
        <span className="font-semibold text-white">
          {totalMessages.toLocaleString()}
        </span>{" "}
        messages, and involved{" "}
        <span className="font-semibold text-white">{users.length}</span>{" "}
        people.
      </p>
    </FadeIn>

    {/* ACT III — DRAMATIC PAUSE */}
    <FadeIn delay={1.1}>
      <div className="w-24 h-1 bg-gradient-to-r from-cyan-400 to-purple-500 rounded-full my-10" />
    </FadeIn>

    {/* ACT IV — SUPPORTING DETAILS */}
    <FadeIn delay={1.5}>
      <p className="text-xl text-gray-400 max-w-4xl">
        Every message, every word, every late-night reply —
        all captured, analyzed, and visualized.
      </p>
    </FadeIn>

    {/* ACT V — FOOTNOTE STATS (SUBTLE) */}
    <FadeIn delay={2.0}>
      <div className="flex gap-10 mt-12 text-gray-400 text-lg">
        <span>
          📝 <span className="text-white font-medium">{totalWords.toLocaleString()}</span> words
        </span>
        <span>
          🔠 <span className="text-white font-medium">{totalChars.toLocaleString()}</span> characters
        </span>
      </div>
    </FadeIn>

    {/* ACT VI — CAST */}
    <FadeIn delay={2.4}>
      <p className="mt-10 text-gray-500 text-lg max-w-5xl">
        Featuring:{" "}
        <span className="text-gray-300">
          {users.join(" • ")}
        </span>
      </p>
    </FadeIn>

  </div>
);

  function StatCard({ label, value }) {
  return (
    <div className="bg-slate-800/70 backdrop-blur-md p-6 rounded-2xl shadow-lg min-w-[160px]">
      <p className="text-gray-400 text-sm uppercase tracking-wide">{label}</p>
      <p className="text-4xl font-bold mt-2">{value}</p>
    </div>
  );
}
}
