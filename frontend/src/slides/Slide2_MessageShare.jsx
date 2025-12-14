import React from "react";
import { PieChart, Pie, Tooltip, Cell, ResponsiveContainer } from "recharts";
import FadeIn from "../components/FadeIn";
import TypingHeader from "../components/TypingHeader";

// Modern color palette
const COLORS = ["#4ade80", "#60a5fa", "#f472b6", "#facc15", "#34d399", "#a78bfa"];

export default function Slide2_MessageShare({ data }) {
  if (!data || !Object.keys(data.total_messages || {}).length)
    return <p>No data available</p>;


  const msgCount = data.total_messages;

  const chartData = Object.entries(msgCount).map(([user, count]) => ({
    name: user,
    value: count,
  }));

  // Determine the most active user
  const entries = Object.entries(msgCount);
  const mostActive = entries.length
    ? entries.reduce((a, b) => (a[1] > b[1] ? a : b))
    : null;

  return (
    <div className="text-white">
      <TypingHeader text="Message Distribution" />

      <FadeIn delay={0.2}>
        <p className="text-lg text-gray-300 max-w-2xl mt-4">
          {mostActive
            ? `💬 ${mostActive[0]} is the most active participant with ${mostActive[1]} messages —
              contributing ${(mostActive[1] / entries.reduce((t, x) => t + x[1], 0) * 100).toFixed(1)}%
              of the entire conversation.`
            : "No active users found."}
        </p>
      </FadeIn>

      <FadeIn delay={0.4}>
        <div className="w-full flex justify-center mt-10">
          <div className="w-[350px] h-[350px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  innerRadius={80}
                  outerRadius={140}
                  paddingAngle={3}
                  dataKey="value"
                  label
                >
                  {chartData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </FadeIn>
    </div>
  );
}
