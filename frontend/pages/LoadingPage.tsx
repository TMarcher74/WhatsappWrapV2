import { getFullAnalysis } from "../lib/api";
import { useEffect } from "react";
import { motion } from "framer-motion";

export default function LoadingPage({ fileId, setStage, setAnalysis }) {

  useEffect(() => {
    async function load() {
      const data = await getFullAnalysis(fileId);
      setAnalysis(data);
      setStage("wrapped");
    }
    load();
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="min-h-screen flex justify-center items-center text-3xl font-semibold"
    >
      Analysing your chat...
    </motion.div>
  );
}
