import React from "react";
import { FileUp } from "lucide-react";

export default function FileUpload({ onUpload, disabled }) {
  const handleChange = (e) => {
    if (!disabled && e.target.files[0]) {
      onUpload(e.target.files[0]);
    }
  };

  return (
    <label
      className={
        `cursor-pointer w-full flex items-center justify-center p-6
         rounded-2xl border-2 border-dashed transition-all
         ${disabled ? "border-gray-600 opacity-40 cursor-not-allowed" :
                      "border-white/40 hover:bg-white/10 hover:border-white"}`
      }
    >
      <div className="flex flex-col items-center text-white">
        <FileUp className="w-10 h-10 mb-2" />
        <p className="text-lg">Click to Upload WhatsApp Chat (.txt)</p>
      </div>
      <input
        type="file"
        accept=".txt"
        onChange={handleChange}
        disabled={disabled}
        className="hidden"
      />
    </label>
  );
}
