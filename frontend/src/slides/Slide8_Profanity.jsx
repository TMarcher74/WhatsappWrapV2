import React from "react";
import SlideWrapper from "../components/SlideWrapper";
import ChartCard from "../components/ChartCard";
import { PieChart, Pie, Tooltip, Cell, ResponsiveContainer } from "recharts";
import FadeIn from "../components/FadeIn";

const COLORS = [
  "#ff6b6b", "#ffa36c", "#ffd93d",
  "#6bcff6", "#7b6bff", "#ff6bcb",
  "#4ade80", "#60a5fa"
];
const profanity = data.profanity || {};


export default function Slide8_Profanity({ data }) {
  if (!data) return null;

  const perUser = data.profanity_user || {};
  const global = data.profanity_global || {};

  // Pie chart data
const chartData = Object.entries(profanity).map(([user, words]) => ({
  name: user,
  value: Object.values(words || {}).reduce((a, b) => a + b, 0),
}));


const globalCounts = {};
Object.values(profanity).forEach((words) => {
  Object.entries(words || {}).forEach(([word, count]) => {
    globalCounts[word] = (globalCounts[word] || 0) + count;
  });
});

const topWords = Object.entries(globalCounts)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 12);


  return (
    <SlideWrapper>
      <ChartCard title="Profanity Breakdown">
        <FadeIn delay={0.2}>
          <p className="text-gray-300 text-lg mb-4">
            A breakdown of profanity usage by each participant.
            The chart shows how often each user used words from your profanity list.
          </p>
        </FadeIn>

        {/* Pie Chart */}
        <div className="w-full h-80">
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={chartData}
                dataKey="value"
                nameKey="name"
                outerRadius={120}
                label
              >
                {chartData.map((entry, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Top profanity words */}
        <FadeIn delay={0.4}>
          <h2 className="text-xl font-semibold mt-10 mb-3">Top Profanity Words</h2>
          {topWords.length === 0 ? (
            <p className="text-gray-400">No profanity detected. Good job everyone 😇</p>
          ) : (
            <div className="grid grid-cols-2 gap-3 text-white">
              {topWords.map(([word, count]) => (
                <div
                  key={word}
                  className="bg-gray-800 p-3 rounded-xl flex justify-between"
                >
                  <span className="font-medium">{word}</span>
                  <span className="text-green-400">{count}</span>
                </div>
              ))}
            </div>
          )}
        </FadeIn>

      </ChartCard>
    </SlideWrapper>
  );
}
