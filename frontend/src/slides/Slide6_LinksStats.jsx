import React from "react";
import SlideWrapper from "../components/SlideWrapper";
import ChartCard from "../components/ChartCard";
import {
  BarChart,
  Bar,
  Tooltip,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

export default function Slide6_LinksStats({ data }) {
  const links = data?.links || {};
  const detailedLinks = data?.detailed_links || {};

  // ---------------- USER WISE LINKS ----------------
  const barData = Object.entries(links).map(([user, count]) => ({
    user,
    count
  }));

  // ---------------- PLATFORM DISTRIBUTION ----------------
  let platformTotals = {};
  let grandTotal = 0;


Object.values(detailedLinks || {}).forEach(([platformCounts]) => {
  Object.entries(platformCounts || {}).forEach(([platform, count]) => {
    platformTotals[platform] = (platformTotals[platform] || 0) + count;
    grandTotal += count;
  });
});


  const platformList = Object.entries(platformTotals)
    .map(([platform, count]) => ({
      platform,
      count,
      percent: ((count / grandTotal) * 100).toFixed(1)
    }))
    .sort((a, b) => b.count - a.count);

  return (
    <SlideWrapper>
      <div className="flex flex-col lg:flex-row gap-10">

        {/* -------- LEFT: BAR CHART -------- */}
        <div className="flex-1">
          <ChartCard title="🔗 Links Sent by Each User">
            <ResponsiveContainer width="100%" height={350}>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
                <XAxis
                  dataKey="user"
                  stroke="#cbd5e1"
                  angle={-20}
                  textAnchor="end"
                />
                <YAxis stroke="#cbd5e1" />
                <Tooltip
                  contentStyle={{ backgroundColor: "#0f172a", border: "none" }}
                  labelStyle={{ color: "#60a5fa" }}
                />
                <Bar dataKey="count" fill="#60a5fa" />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* -------- RIGHT: PLATFORM LIST -------- */}
        <div className="flex-1">
          <ChartCard title="🌍 Platforms Shared (Ranked)">
            <div className="max-h-[350px] overflow-y-auto pr-3 space-y-3">

              {platformList.length === 0 && (
                <p className="text-gray-300 text-center">No links found</p>
              )}

              {platformList.map((item, idx) => (
                <div key={idx} className="bg-slate-800 p-3 rounded-xl">
                  <div className="flex justify-between text-white text-sm mb-1">
                    <span>{item.platform}</span>
                    <span>{item.count} links ({item.percent}%)</span>
                  </div>

                  <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-green-400"
                      style={{ width: `${item.percent}%` }}
                    />
                  </div>
                </div>
              ))}

            </div>
          </ChartCard>
        </div>

      </div>
    </SlideWrapper>
  );
}
