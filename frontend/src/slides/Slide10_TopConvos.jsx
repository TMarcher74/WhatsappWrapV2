import React from "react";
import SlideWrapper from "../components/SlideWrapper";
import ChartCard from "../components/ChartCard";
import FadeIn from "../components/FadeIn";

export default function Slide10_TopConvos({ data }) {
  if (!data || !data.convos) {
    return (
      <SlideWrapper>
        <p className="text-gray-400 text-center">No conversation data available.</p>
      </SlideWrapper>
    );
  }

  // Remove metadata like "gap threshold in seconds"
  const conversations = Object.entries(data.convos)
    .filter(([key, val]) => typeof val === "object" && val.start)
    .map(([title, convo]) => ({ title, ...convo }));

  if (conversations.length === 0) {
    return (
      <SlideWrapper>
        <p className="text-gray-400 text-center">No conversation data available.</p>
      </SlideWrapper>
    );
  }

  return (
    <SlideWrapper>
      <h2 className="text-4xl font-bold text-white text-center mb-8">
        💬 Top Conversations
      </h2>

      <div className="space-y-8">
        {conversations.map((convo, idx) => (
          <FadeIn key={idx} delay={idx * 0.1}>
            <ChartCard title={convo.title}>

              {/* META INFO */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-300 mb-4">
                <div>
                  <b className="text-white">Start</b>
                  <div>{new Date(convo.start).toLocaleString()}</div>
                </div>
                <div>
                  <b className="text-white">End</b>
                  <div>{new Date(convo.end).toLocaleString()}</div>
                </div>
                <div>
                  <b className="text-white">Duration</b>
                  <div>{convo.duration_min} min</div>
                </div>
                <div>
                  <b className="text-white">Messages</b>
                  <div>{convo.messages}</div>
                </div>
              </div>

              {/* PARTICIPANTS */}
              <div className="mb-4">
                <b className="text-white">Participants:</b>
                <div className="flex flex-wrap gap-2 mt-1">
                  {convo.participants.map((p) => (
                    <span
                      key={p}
                      className="px-3 py-1 text-xs rounded-full bg-slate-700 text-white"
                    >
                      {p}
                    </span>
                  ))}
                </div>
              </div>

              {/* SCROLLABLE MESSAGE WINDOW (LIKE SLIDE 6) */}
              <div className="max-h-[320px] overflow-y-auto pr-2 space-y-2 bg-slate-900 rounded-xl p-3">
                {convo.conversation.map(([time, user, message], i) => (
                  <div
                    key={i}
                    className="text-sm text-gray-200 bg-slate-800 p-2 rounded-lg"
                  >
                    <div className="text-xs text-gray-400 mb-1">
                      {new Date(time).toLocaleTimeString()} · <b>{user}</b>
                    </div>
                    <div>{message}</div>
                  </div>
                ))}
              </div>

            </ChartCard>
          </FadeIn>
        ))}
      </div>
    </SlideWrapper>
  );
}
