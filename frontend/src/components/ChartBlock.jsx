// src/components/ChartBlock.jsx
import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  LabelList,
} from "recharts";

/**
 * ChartBlock
 * Props:
 *  - title: string
 *  - data: Array<{ name: string, value: number }>
 *  - color: string (tailwind / hex)
 */
export default function ChartBlock({ title, data = [], color = "#60a5fa" }) {
  // Defensive: ensure data is an array of objects with name/value
  const sanitized = Array.isArray(data)
    ? data.map((d) => ({ name: String(d.name || ""), value: Number(d.value || 0) }))
    : [];

  return (
    <div className="bg-gray-900/60 rounded-xl p-6 shadow-md">
      <h3 className="text-2xl font-semibold mb-4 text-white">{title}</h3>

      {sanitized.length === 0 ? (
        <p className="text-gray-400">No data available</p>
      ) : (
        <div style={{ width: "100%", height: 320 }}>
          <ResponsiveContainer>
            <BarChart data={sanitized} margin={{ top: 10, right: 16, left: -12, bottom: 60 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
              <XAxis
                dataKey="name"
                interval={0}
                angle={-35}
                textAnchor="end"
                height={70}
                tick={{ fill: "#d1d5db", fontSize: 12 }}
              />
              <YAxis tick={{ fill: "#d1d5db", fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="value" fill={color} radius={[6, 6, 0, 0]}>
                <LabelList dataKey="value" position="top" formatter={(v) => (v ? v : "")} />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
