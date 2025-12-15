import React from "react";
import SlideWrapper from "../components/SlideWrapper";
import ChartCard from "../components/ChartCard";
import { PieChart, Pie, Tooltip, Cell, ResponsiveContainer } from "recharts";
import ReactWordcloud from "react-wordcloud";
import FadeIn from "../components/FadeIn";

const COLORS = [
  "#ff6b6b", "#ffa36c", "#ffd93d",
  "#6bcff6", "#7b6bff", "#ff6bcb",
  "#4ade80", "#60a5fa"
];

export default function Slide8_Profanity({ data }) {
  if (!data?.profanity) return null;

  const profanity = data.profanity;

  /* ---------------- PIE DATA (User-wise) ---------------- */
  const pieData = Object.entries(profanity).map(([user, stats]) => ({
    name: user,
    value: stats.total_p_words || 0,
  })).filter(d => d.value > 0);

  /* ---------------- WORD CLOUD DATA ---------------- */
  const globalWordCounts = {};

  Object.values(profanity).forEach(userData => {
    Object.entries(userData.canonical || {}).forEach(([word, meta]) => {
      globalWordCounts[word] =
        (globalWordCounts[word] || 0) + (meta.count || 0);
    });
  });

  const wordCloudData = Object.entries(globalWordCounts)
    .map(([text, value]) => ({ text, value }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 50); // limit for readability

  /* ---------------- WORD CLOUD OPTIONS ---------------- */
  const wordCloudOptions = {
    rotations: 2,
    rotationAngles: [0, 0],
    fontSizes: [18, 70],
    padding: 2,
    enableTooltip: true,
  };

  return (
    <SlideWrapper>
      <ChartCard title="😡 Profanity Breakdown">

        <FadeIn delay={0.2}>
          <p className="text-gray-300 text-lg mb-6 max-w-3xl">
            This slide shows how often profanity appeared in the conversation.
            The pie chart represents user-wise usage, while the word cloud highlights
            the most frequently used profane words.
          </p>
        </FadeIn>

        {/* ---------------- PIE CHART ---------------- */}
        <div className="w-full h-[420px] flex justify-center items-center mb-12">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={pieData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                innerRadius={70}
                outerRadius={120}
                paddingAngle={2}
                labelLine={false}
                label={({ value }) => value}
              >
                {pieData.map((_, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* ---------------- WORD CLOUD ---------------- */}
        <FadeIn delay={0.4}>
          <h2 className="text-2xl font-semibold text-white text-center mb-6">
            Most Used Profanity
          </h2>

          {wordCloudData.length === 0 ? (
            <p className="text-gray-400 text-center">
              No profanity detected. Everyone behaved 😇
            </p>
          ) : (
            <div className="w-full h-[320px] bg-slate-900 rounded-xl p-4">
              <ReactWordcloud
                words={wordCloudData}
                options={wordCloudOptions}
              />
            </div>
          )}
        </FadeIn>

      </ChartCard>
    </SlideWrapper>
  );
}
