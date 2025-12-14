import React from "react";
import { motion } from "framer-motion";

export default function SlideWrapper({ children }) {
  return (
    <motion.div
      className="w-full min-h-screen py-20 flex justify-center items-center"
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.4 }}
      transition={{ duration: 0.7, ease: "easeOut" }}
    >
      <div className="w-full max-w-5xl bg-white/10 backdrop-blur-xl p-12 rounded-2xl shadow-xl border border-white/20">
        {children}
      </div>
    </motion.div>
  );
}
