import React, { useState } from "react";
import { motion } from "framer-motion";
import { FaWhatsapp } from "react-icons/fa";

export default function LandingPage({ onUpload }) {
  const [accepted, setAccepted] = useState(false);
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleContinue = () => {
    if (accepted && file) onUpload(file);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-white relative overflow-hidden">

      {/* 🔥 Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-green-500 via-emerald-600 to-black opacity-90"></div>

      {/* ✨ Floating WhatsApp Icon */}
      <motion.div
        initial={{ y: -20 }}
        animate={{ y: 20 }}
        transition={{ repeat: Infinity, duration: 2, ease: "easeInOut", repeatType: "reverse" }}
        className="absolute top-10 text-white/40 text-[140px]"
      >
        <FaWhatsapp />
      </motion.div>

      {/* 🟩 Main Card */}
      <div className="relative z-10 w-[90%] max-w-3xl bg-white/10 backdrop-blur-md p-10 rounded-3xl shadow-2xl border border-white/20">

        <h1 className="text-4xl font-bold mb-4 text-center">
          WhatsApp Wrap 2024 📱✨
        </h1>

        {/* Website description */}
        <p className="text-lg mb-6 text-center text-gray-200 leading-relaxed">
          WhatsApp Wrap transforms your chat history into beautiful insights —
          showing your message trends, emojis used, active hours, funniest moments,
          milestones and more.
          <br />
          <br />
          Everything is analysed instantly and visually in a **slide-based story format**
          just like Spotify Wrapped 🎉
        </p>

        {/* Privacy Policy Header */}
        <h2 className="text-2xl font-semibold mb-3 text-emerald-300">Privacy Policy</h2>

        {/* Privacy Content */}
        <div className=" max-h-64 overflow-y-auto pr-2 text-gray-200 space-y-4 text-sm leading-relaxed">
          <p>
            This page informs you of our policies regarding the collection, use, and
            disclosure of personal data when you use our Service and the choices you
            have associated with that data.
          </p>

          <h3 className="text-xl font-semibold text-emerald-300">Information Collection and Use</h3>
          <p>
            We <b><u>do not</u></b> collect any data. Everything happens on the client-side.
          </p>

          <h3 className="text-xl font-semibold text-emerald-300">Types of Data Collected</h3>

          <h4 className="text-lg font-semibold text-emerald-200">Personal Data</h4>
          <p>No personal data is collected.</p>

          <h4 className="text-lg font-semibold text-emerald-200">Usage Data</h4>
          <p>No usage data is collected.</p>

          <h4 className="text-lg font-semibold text-emerald-200">Tracking & Cookies Data</h4>
          <p>This website does not use cookies or tracking data.</p>

          <h3 className="text-xl font-semibold text-emerald-300">Contact Us</h3>
          <p>
            If you have any questions about this Privacy Policy, please contact us at:<br />
            <b>whatsappwrap13@gmail.com</b>
          </p>
        </div>

        {/* Consent Checkbox */}
        <div className="mt-6 flex items-center space-x-3">
          <input
            type="checkbox"
            id="consent"
            className="w-5 h-5"
            checked={accepted}
            onChange={() => setAccepted(!accepted)}
          />
          <label htmlFor="consent" className="text-gray-200 text-sm">
            I understand and agree to proceed with the analysis.
          </label>
        </div>

        {/* File Upload */}
        <div className="mt-6">
          <input
            type="file"
            accept=".txt"
            onChange={handleFileChange}
            className="text-gray-200"
            disabled={!accepted}
          />
        </div>

        {/* Modern Upload Button */}
        <button
          onClick={handleContinue}
          disabled={!accepted || !file}
          className={`mt-6 w-full py-3 rounded-xl text-lg font-semibold transition-all duration-300
            ${
              accepted && file
                ? "bg-emerald-500 hover:bg-emerald-600 shadow-lg"
                : "bg-gray-500 cursor-not-allowed opacity-50"
            }`}
        >
          Upload & Generate Wrap 🎉
        </button>
      </div>
    </div>
  );
}
