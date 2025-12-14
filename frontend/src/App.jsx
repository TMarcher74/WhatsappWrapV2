import React, { useState } from "react";
import LandingPage from "./components/LandingPage";
import Sidebar from "./components/Sidebar";
import ProgressBar from "./components/ProgressBar";
import FadeIn from "./components/FadeIn";
import SlideNumber from "./components/SlideNumber";
import TypingHeader from "./components/TypingHeader";

import { normalizeAnalysis } from "./util/normalizeAnalysis";

import Slide1_Overview from "./slides/Slide1_Overview";
import Slide2_MessageShare from "./slides/Slide2_MessageShare";
import Slide3_UserBreakdown from "./slides/Slide3_UserBreakdown";
import Slide4_ActiveHours from "./slides/Slide4_ActiveHours";
import Slide5_MessageQuality from "./slides/Slide5_MessageQuality";
import Slide6_LinksStats from "./slides/Slide6_LinksStats";
import Slide7_InteractionGraph from "./slides/Slide7_InteractionGraph";
// import Slide8_Profanity from "./slides/Slide8_Profanity";

export default function App() {
  const [data, setData] = useState(null);
  const [expanded, setExpanded] = useState(false);
  const [analysis, setAnalysis] = useState(null);

  const slideWidthOffset = expanded ? 260 : 72;

  const slides = [
    { id: "slide1", component: <Slide1_Overview data={data} /> },
    { id: "slide2", component: <Slide2_MessageShare data={data} /> },
    { id: "slide3", component: <Slide3_UserBreakdown data={data} /> },
{ id: "slide4", component: <Slide4_ActiveHours data={data} /> },
{ id: "slide5", component: <Slide5_MessageQuality data={data} /> },
 { id: "slide6", component: <Slide6_LinksStats data={data} /> },
    { id: "slide7", component: <Slide7_InteractionGraph data={data} /> }
//     { id: "slide8", component: <Slide8_Profanity data={data} /> }
  ];

  async function handleUpload(file) {
    try {
      const formData = new FormData();
      formData.append("file", file);

      // STEP 1 — Upload
      const uploadRes = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      const uploadJson = await uploadRes.json();
      const fileId = uploadJson.file_id;

      // STEP 2 — Analyse
      const analyseRes = await fetch(
        `http://127.0.0.1:8000/analyse/all/${fileId}`,
        { method: "POST" }
      );

const analyseJson = await analyseRes.json();
console.log("RAW ANALYSE DATA:", analyseJson);

const normalized = normalizeAnalysis(analyseJson);
console.log("NORMALIZED DATA:", normalized);

setData(normalized);

    } catch (err) {
      console.error("Upload/Analyse error:", err);
    }
  }

  function navigateToSlide(id) {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
  }

  if (!data) {
    return <LandingPage onUpload={handleUpload} />;
  }

return (
  <div className="flex">

    <Sidebar
      expanded={expanded}
      setExpanded={setExpanded}
      onNavigate={navigateToSlide}
    />

    <ProgressBar />

    {/* ⭐ ADD THIS HERE (slide number indicator) */}
    <SlideNumber slides={slides.length} />

<div
  className="flex-1 h-screen snap-y snap-mandatory overflow-y-auto"
  style={{ marginLeft: slideWidthOffset, transition: "margin 0.3s ease" }}
>

      {slides.map((s, index) => (
<section
  id={s.id}
  key={s.id}
  className="min-h-screen snap-start p-10 flex flex-col"
>
  {s.component}
</section>

))}

    </div>

  </div>
);

}
