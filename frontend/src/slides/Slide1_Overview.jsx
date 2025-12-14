import React from "react";
import TypingHeader from "../components/TypingHeader";
import FadeIn from "../components/FadeIn";

export default function Slide1_Overview({ data }) {
  if (!data) return null;

  const users = data.users || [];
const totalMessages = Object.values(data.total_messages || {})
  .reduce((a, b) => a + b, 0);

const totalWords = Object.values(data.word_character_stats || {})
  .reduce((a, b) => a + (b?.words || 0), 0);

const totalChars = Object.values(data.word_character_stats || {})
  .reduce((a, b) => a + (b?.characters || 0), 0);


  const activeDays = Object.keys(data.date_frequency || {}).length;

  return (
    <>
      <TypingHeader text="WhatsApp Chat Overview" />

      <FadeIn delay={0.2}>
        <p><b>Participants:</b> {users.join(", ")}</p>
      </FadeIn>

      <FadeIn delay={0.3}>
        <p><b>Total Messages:</b> {totalMessages}</p>
      </FadeIn>

      <FadeIn delay={0.4}>
        <p><b>Total Words:</b> {totalWords}</p>
      </FadeIn>

      <FadeIn delay={0.5}>
        <p><b>Total Characters:</b> {totalChars}</p>
      </FadeIn>

      <FadeIn delay={0.6}>
        <p><b>Active Chat Days:</b> {activeDays}</p>
      </FadeIn>
    </>
  );
}
