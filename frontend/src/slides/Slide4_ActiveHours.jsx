import React, { useState } from "react";
import SlideWrapper from "../components/SlideWrapper";
import ChartCard from "../components/ChartCard";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  BarChart,
  Bar,
} from "recharts";

export default function Slide4_ActiveHours({ data }) {
  const timeFreq = data?.time_frequency || {};

  const chartData = Object.entries(timeFreq).map(([hour, count]) => ({
    hour: `${hour}:00`,
    messages: count,
  }));

  // Find busiest hour
  const busiest = chartData.reduce(
    (max, curr) => (curr.messages > max.messages ? curr : max),
    { messages: 0 }
  );

  const [mode, setMode] = useState("line"); // "line" or "bar"

  return (
    <SlideWrapper>
      <ChartCard title="⏰ Hourly Activity">

        {/* Toggle */}
        <div className="flex justify-end mb-3">
          <button
            onClick={() => setMode(mode === "line" ? "bar" : "line")}
            className="px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-600 transition"
          >
            Switch to {mode === "line" ? "Bar Chart" : "Line Chart"}
          </button>
        </div>

        <p className="text-center text-xl text-white mb-4">
          Busiest Hour: <span className="font-bold text-yellow-400">
            {busiest.hour} 🔥
          </span>
          {"  "}with {busiest.messages} messages
        </p>

        <ResponsiveContainer width="100%" height={350}>
          {mode === "line" ? (
            /* ---------------- LINE CHART ---------------- */
            <LineChart data={chartData}>
              <defs>
                <linearGradient id="colorMessages" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="20%" stopColor="#38bdf8" stopOpacity={0.8} />
                  <stop offset="90%" stopColor="#38bdf8" stopOpacity={0.05} />
                </linearGradient>
              </defs>

              <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
              <XAxis dataKey="hour" stroke="#cbd5e1" />
              <YAxis stroke="#cbd5e1" />
              <Tooltip
                contentStyle={{ backgroundColor: "#0f172a", border: "none" }}
                labelStyle={{ color: "#38bdf8" }}
              />

              <Line
                type="monotone"
                dataKey="messages"
                stroke="#38bdf8"
                strokeWidth={3}
                dot={{ r: 4 }}
                activeDot={{ r: 7 }}
                fill="url(#colorMessages)"
                animationDuration={700}
              />
            </LineChart>
          ) : (
            /* ---------------- BAR CHART ---------------- */
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
              <XAxis dataKey="hour" stroke="#cbd5e1" />
              <YAxis stroke="#cbd5e1" />
              <Tooltip
                contentStyle={{ backgroundColor: "#0f172a", border: "none" }}
                labelStyle={{ color: "#38bdf8" }}
              />
              <Bar dataKey="messages" fill="#60a5fa" />
            </BarChart>
          )}
        </ResponsiveContainer>
      </ChartCard>
    </SlideWrapper>
  );
}
