// src/slides/Slide3_UserBreakdown.jsx
import React from "react";
import ChartBlock from "../components/ChartBlock";
import TypingHeader from "../components/TypingHeader"; // optional if you have it
import FadeIn from "../components/FadeIn"; // optional

export default function Slide3_UserBreakdown({ data }) {
  if (!data) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <p className="text-gray-400">Upload a chat file to see user breakdown.</p>
      </div>
    );
  }

  // word_character_stats expected shape: { <user>: { messages, sentences, words, characters, "words/message", "words/sentence", "characters/word" } }
  const wc = data.word_character_stats || {};

  // build arrays for charts
  const users = Object.keys(wc);

  const messagesData = users.map((u) => ({ name: u, value: wc[u]?.messages ?? 0 }));
  const sentencesData = users.map((u) => ({ name: u, value: wc[u]?.sentences ?? 0 }));
  const wordsData = users.map((u) => ({ name: u, value: wc[u]?.words ?? 0 }));
  const charsData = users.map((u) => ({ name: u, value: wc[u]?.characters ?? 0 }));

  // compute aggregate stats if you want per-chat averages (fall back gracefully)
  // NEW: Per-user ratios
const wordsPerMessageData = users.map((u) => ({
  name: u,
  value: wc[u]?.["words/message"] ?? 0,
}));

const wordsPerSentenceData = users.map((u) => ({
  name: u,
  value: wc[u]?.["words/sentence"] ?? 0,
}));

const charsPerWordData = users.map((u) => ({
  name: u,
  value: wc[u]?.["characters/word"] ?? 0,
}));





  return (
    <div className="space-y-10 w-full">
      {/** Header */}
      <div className="flex items-center justify-between">
        {typeof TypingHeader === "function" ? (
          <TypingHeader text="User Breakdown" />
        ) : (
          <h2 className="text-3xl font-bold text-white">User Breakdown</h2>
        )}
      </div>

      {/** Charts stacked vertically */}
      <div className="grid grid-cols-1 gap-10">
        <ChartBlock title="Messages Sent by Each User" data={messagesData} color="#60a5fa" />
        <ChartBlock title="Sentences Sent by Each User" data={sentencesData} color="#34d399" />
        <ChartBlock title="Words Sent by Each User" data={wordsData} color="#f472b6" />
        <ChartBlock title="Characters Sent by Each User" data={charsData} color="#a78bfa" />
<ChartBlock title="Words per Message" data={wordsPerMessageData} />
<ChartBlock title="Words per Sentence" data={wordsPerSentenceData} />
<ChartBlock title="Characters per Word" data={charsPerWordData} />
      </div>
    </div>
  );
}
