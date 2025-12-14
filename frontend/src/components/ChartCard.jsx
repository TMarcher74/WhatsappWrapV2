import React from "react";

export default function ChartCard({ title, children }) {
return (
<div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 w-[90%] max-w-3xl shadow-xl mb-8">
<h2 className="text-xl font-bold mb-4 text-white text-center">{title}</h2>
<div className="w-full flex justify-center">{children}</div>
</div>
);
}