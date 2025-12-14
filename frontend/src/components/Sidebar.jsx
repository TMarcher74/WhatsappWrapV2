import React, { useState } from "react";
import { FaHome, FaSmile, FaFont, FaClock, FaUsers, FaPhotoVideo, FaStar, FaLaugh, FaBars } from "react-icons/fa";

export default function Sidebar({ activeSlide, onNavigate, expanded, setExpanded }) {

  const menu = [
    { id: "slide1", label: "Overview", icon: <FaHome /> },
    { id: "slide2", label: "Emojis", icon: <FaSmile /> },
    { id: "slide3", label: "Top Words", icon: <FaFont /> },
    { id: "slide4", label: "Active Hours", icon: <FaClock /> },
    { id: "slide5", label: "Contacts", icon: <FaUsers /> },
    { id: "slide6", label: "Media", icon: <FaPhotoVideo /> },
    { id: "slide7", label: "Milestones", icon: <FaStar /> },
    { id: "slide8", label: "Summary", icon: <FaLaugh /> },
  ];

  return (
    <div
      className={`h-screen fixed top-0 left-0 bg-gray-900 text-white shadow-xl
        transition-all duration-300 ease-in-out
      `}
      style={{
        width: expanded ? 260 : 72,
      }}
    >
      {/* Toggle Button */}
      <div
        className="flex items-center gap-3 p-4 cursor-pointer hover:bg-gray-800"
        onClick={() => setExpanded(!expanded)}
      >
        <FaBars className="text-xl" />
        {expanded && <span className="text-lg font-semibold">Menu</span>}
      </div>

      {/* Menu Items */}
      <div className="mt-2">
        {menu.map((item) => (
          <div
            key={item.id}
            onClick={() => onNavigate(item.id)}
            className={`flex items-center gap-3 p-4 cursor-pointer transition-all
              ${activeSlide === item.id ? "bg-green-600" : "hover:bg-gray-800"}
            `}
          >
            <span className="text-xl">{item.icon}</span>
            {expanded && <span className="text-md">{item.label}</span>}
          </div>
        ))}
      </div>
    </div>
  );
}
