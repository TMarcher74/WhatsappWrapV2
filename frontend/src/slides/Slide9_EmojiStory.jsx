import React from "react";
import SlideWrapper from "../components/SlideWrapper";
import FadeIn from "../components/FadeIn";
import TypingHeader from "../components/TypingHeader";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

export default function Slide9_EmojiStory({ data }) {
  if (!data?.emojis_emoticons_used) {
    return (
      <SlideWrapper>
        <p className="text-gray-400 text-center text-xl">
          No emoji or emoticon usage detected.
        </p>
      </SlideWrapper>
    );
  }

  /* ---------------- AGGREGATE DATA ---------------- */

  const emojiTotals = {};
  const emoticonTotals = {};

  Object.values(data.emojis_emoticons_used).forEach(([emojiMap, emoticonMap]) => {
    Object.entries(emojiMap || {}).forEach(([emoji, count]) => {
      emojiTotals[emoji] = (emojiTotals[emoji] || 0) + count;
    });

    Object.entries(emoticonMap || {}).forEach(([emo, count]) => {
      emoticonTotals[emo] = (emoticonTotals[emo] || 0) + count;
    });
  });

  const sortedEmojis = Object.entries(emojiTotals).sort((a, b) => b[1] - a[1]);
  const sortedEmoticons = Object.entries(emoticonTotals).sort((a, b) => b[1] - a[1]);

  const topEmoji = sortedEmojis[0];
  const topEmoticon = sortedEmoticons[0];

  const emojiChartData = sortedEmojis.slice(0, 8).map(([k, v]) => ({
    symbol: k,
    count: v,
  }));

  /* ---------------- RENDER ---------------- */

  return (
    <SlideWrapper>

      <TypingHeader text="The Language Beyond Words" />

      {/* STORY */}
      <FadeIn delay={0.4}>
        <p className="text-2xl text-gray-200 max-w-4xl mt-8 leading-relaxed">
          Not everything was said with words.
          Emotions leaked through reactions, pauses, and symbols.
        </p>
      </FadeIn>

      {/* HIGHLIGHTS */}
      <FadeIn delay={0.9}>
        <div className="flex flex-col md:flex-row gap-16 mt-12 text-xl text-gray-300">
          {topEmoji && (
            <span>
              Most used emoji:{" "}
              <span className="text-white font-semibold text-3xl">
                {topEmoji[0]}
              </span>{" "}
              ({topEmoji[1]} times)
            </span>
          )}

          {topEmoticon && (
            <span>
              Most used emoticon:{" "}
              <span className="text-white font-semibold">
                {topEmoticon[0]}
              </span>{" "}
              ({topEmoticon[1]} times)
            </span>
          )}
        </div>
      </FadeIn>

      {/* VISUAL — EMOJI FREQUENCY */}
      <FadeIn delay={1.4}>
        <div className="w-full h-[360px] mt-12">
          <ResponsiveContainer>
            <BarChart data={emojiChartData}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
              <XAxis dataKey="symbol" stroke="#cbd5e1" />
              <YAxis stroke="#cbd5e1" />
              <Tooltip
                contentStyle={{ backgroundColor: "#0f172a", border: "none" }}
                labelStyle={{ color: "#38bdf8" }}
              />
              <Bar dataKey="count" fill="#facc15" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </FadeIn>

      {/* CLOSING LINE */}
      <FadeIn delay={1.9}>
        <p className="text-gray-400 text-lg mt-10 max-w-4xl">
          These small symbols quietly carried tone, sarcasm, laughter,
          and sometimes what words couldn’t.
        </p>
      </FadeIn>

    </SlideWrapper>
  );
}
