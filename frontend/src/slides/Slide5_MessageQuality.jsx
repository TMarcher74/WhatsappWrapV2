import React from "react";
import SlideWrapper from "../components/SlideWrapper";
import {
  PieChart,
  Pie,
  Tooltip,
  Legend,
  Cell,
  ResponsiveContainer,
} from "recharts";

const COLORS = [
  "#60a5fa",
  "#34d399",
  "#f472b6",
  "#facc15",
  "#a78bfa",
  "#fb7185",
  "#4ade80",
];

function PieBlock({ title, data }) {
  return (
    <div className="bg-slate-800 p-5 rounded-xl shadow-lg">
      <h3 className="text-xl text-white font-semibold mb-4 text-center">
        {title}
      </h3>

      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            outerRadius={110}
            label
          >
            {data.map((_, idx) => (
              <Cell key={idx} fill={COLORS[idx % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default function Slide5_MessageQuality({ data }) {
  const del = data?.deleted_messages || {};
  const edit = data?.edited_messages || {};
  const media = data?.media || {};

  const deletedData = Object.entries(del).map(([u, c]) => ({
    name: u,
    value: c,
  }));

  const editedData = Object.entries(edit).map(([u, c]) => ({
    name: u,
    value: c,
  }));

  const mediaData = Object.entries(media).map(([u, c]) => ({
    name: u,
    value: c,
  }));

  return (
    <SlideWrapper>
      <h2 className="text-4xl font-bold text-white text-center mb-8">
        🧹 Message Cleanup Summary
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <PieBlock title="🗑 Deleted Messages" data={deletedData} />
        <PieBlock title="✏️ Edited Messages" data={editedData} />
        <PieBlock title="📎 Media Shared" data={mediaData} />
      </div>
    </SlideWrapper>
  );
}
