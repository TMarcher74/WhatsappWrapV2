import React from "react";
import SlideWrapper from "../components/SlideWrapper";
import ChartCard from "../components/ChartCard";
import {   BarChart,
  Bar,
  XAxis,
  YAxis,
  Legend,PieChart, Pie, Tooltip, Cell, ResponsiveContainer } from "recharts";
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

  const worstOffender = Object.entries(profanity)
  .sort((a, b) => b[1].total_p_words - a[1].total_p_words)[0];


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

  const comparisonData = Object.keys(profanity).map(user => ({
  user,
  messages: data.total_messages?.[user] || 0,
  profanity: profanity[user].total_p_words || 0
}));


  return (
  <SlideWrapper>
    <ChartCard title="Profanity Breakdown">

      {/* FORCE COLUMN LAYOUT */}
      <div className="flex flex-col w-full">

        <p className="text-gray-300 text-lg mb-6">
          Profanity usage across participants and the most commonly used words.
        </p>

        <div className="mb-6 text-center">
          <p className="text-xl font-semibold text-red-400">
            🚨 Worst Offender: {worstOffender[0]}
          </p>
          <p className="text-gray-400">
            {worstOffender[1].total_p_words} profane words
            ({worstOffender[1].total_percentage.toFixed(2)}%)
          </p>
        </div>


        {/* ================= PIE CHART ================= */}
        <div className="w-full h-[320px] flex justify-center mb-12">
          <ResponsiveContainer width="70%" height="100%">
            <PieChart>
              <Pie
                data={pieData}
                dataKey="value"
                nameKey="name"
                outerRadius={120}
                labelLine={false}
                label={({ name }) => name}
              >
                {pieData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* ================= WORD CLOUD ================= */}
        <div className="w-full flex justify-center">
          <div className="w-[90%] h-[320px]">
            <ReactWordcloud
              words={wordCloudData}
              options={{
                rotations: 2,
                rotationAngles: [-90, 0],
                fontSizes: [14, 60],
                padding: 4,
                deterministic: true
              }}
            />
          </div>
        </div>

        {/* ================= PROFANITY vs MESSAGE VOLUME ================= */}
        <div className="w-full mt-16">
          <h2 className="text-2xl font-semibold text-center mb-6">
            Profanity vs Message Volume
          </h2>

          <div className="w-full h-[380px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={comparisonData}
                margin={{ top: 20, right: 40, left: 20, bottom: 60 }}
              >
                <XAxis
                  dataKey="user"
                  angle={-25}
                  textAnchor="end"
                  interval={0}
                  height={80}
                />

                {/* Left axis → messages */}
                <YAxis
                  yAxisId="left"
                  orientation="left"
                  stroke="#60a5fa"
                />

                {/* Right axis → profanity */}
                <YAxis
                  yAxisId="right"
                  orientation="right"
                  stroke="#ef4444"
                />

                <Tooltip />
                <Legend />

                <Bar
                  yAxisId="left"
                  dataKey="messages"
                  name="Total Messages"
                  fill="#60a5fa"
                  radius={[6, 6, 0, 0]}
                />

                <Bar
                  yAxisId="right"
                  dataKey="profanity"
                  name="Profanity Words"
                  fill="#ef4444"
                  radius={[6, 6, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </ChartCard>
  </SlideWrapper>
);

}
