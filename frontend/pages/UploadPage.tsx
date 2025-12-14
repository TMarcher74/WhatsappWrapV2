import FileUpload from "../components/FileUpload";
import { uploadFile } from "../lib/api";

export default function UploadPage({ setStage, setFileId }) {
  async function handleUpload(file) {
    const res = await uploadFile(file);
    setFileId(res.file_id);
    setStage("loading");
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-6">WhatsApp Wrapped</h1>
      <FileUpload onUpload={handleUpload} />
    </div>
  );
}
