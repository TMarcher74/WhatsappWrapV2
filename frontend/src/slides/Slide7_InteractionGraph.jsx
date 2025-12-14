import React, { useEffect, useRef } from "react";
import ForceGraph2D from "react-force-graph-2d";

export default function Slide7_InteractionGraph({ data }) {
  const graphRef = useRef();

  if (!data?.mentions) {
    console.warn("❌ No mention data found");
    return <p className="text-white text-xl">No mentions found in chat.</p>;
  }

  const users = data.users || [];
  const mentions = data.mentions || {};

  // NODES
  const nodes = users.map((u) => ({
    id: u,
    name: u,
  }));

  // LINKS
  const links = [];
  for (const [sender, targetMap] of Object.entries(mentions)) {
    if (!targetMap || typeof targetMap !== "object") continue;

    for (const [target, count] of Object.entries(targetMap)) {
      if (!users.includes(target) || count <= 0) continue;

      links.push({
        source: sender,
        target,
        value: count,
      });
    }
  }

  if (links.length === 0) {
    return (
      <p className="text-white text-xl text-center">
        No user mentions detected in this chat.
      </p>
    );
  }

  const graphData = { nodes, links };

  // AUTO-CENTER
  useEffect(() => {
    setTimeout(() => {
      if (graphRef.current) graphRef.current.zoomToFit(800, 50);
    }, 500);
  }, []);

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "rgba(15,23,42,0.9)",
        borderRadius: "20px",
      }}
    >
      <ForceGraph2D
        ref={graphRef}
        graphData={graphData}
        cooldownTicks={50}
        minZoom={0.5}
        maxZoom={3}
        nodeRelSize={4} // smaller node radius
        linkWidth={(link) => Math.min(link.value, 5)}
        linkColor={() => "rgba(0,255,255,0.6)"}
        nodeCanvasObjectMode={() => "after"}
        nodeCanvasObject={(node, ctx, globalScale) => {
          const radius = 6; // smaller node radius

          // Draw node circle
          ctx.beginPath();
          ctx.arc(node.x, node.y, radius, 0, 2 * Math.PI);
          ctx.fillStyle = "rgba(0,255,255,0.85)";
          ctx.shadowBlur = 8;
          ctx.shadowColor = "cyan";
          ctx.fill();

          // reset shadow
          ctx.shadowBlur = 0;

          // TRUE FIX → Adjust label size by zoom
          const fontSize = 6 / globalScale; // ensures tiny font always
          ctx.font = `${fontSize}px Sans-Serif`;
          ctx.fillStyle = "#fff";
          ctx.textAlign = "center";
          ctx.textBaseline = "top";

          // Draw label BELOW node
          ctx.fillText(node.id, node.x, node.y + radius + 2);
        }}
      />
    </div>
  );
}
