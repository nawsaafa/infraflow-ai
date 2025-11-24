"use client";

import { useState, useCallback } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Upload, X, FileText, CheckCircle, AlertCircle } from "lucide-react";

interface FileUploadProps {
  projectId?: string;
  onUploadComplete?: (files: File[]) => void;
}

export function FileUpload({ projectId, onUploadComplete }: FileUploadProps) {
  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<Record<string, "pending" | "success" | "error">>({});

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const droppedFiles = Array.from(e.dataTransfer.files);
    setFiles((prev) => [...prev, ...droppedFiles]);
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      setFiles((prev) => [...prev, ...selectedFiles]);
    }
  };

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    setUploading(true);

    // Simulate upload process
    for (const file of files) {
      setUploadStatus((prev) => ({ ...prev, [file.name]: "pending" }));

      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1000));

      setUploadStatus((prev) => ({ ...prev, [file.name]: "success" }));
    }

    setUploading(false);
    onUploadComplete?.(files);
  };

  return (
    <div className="space-y-4">
      {/* Drop Zone */}
      <div
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-500 transition-colors cursor-pointer"
      >
        <input
          type="file"
          multiple
          onChange={handleFileSelect}
          className="hidden"
          id="file-upload"
          accept=".pdf,.doc,.docx,.xls,.xlsx"
        />
        <label htmlFor="file-upload" className="cursor-pointer">
          <Upload className="h-12 w-12 mx-auto text-gray-400 mb-4" />
          <p className="text-lg font-medium mb-2">Drop files here or click to browse</p>
          <p className="text-sm text-gray-500">
            Supports: PDF, Word, Excel (Max 100MB per file)
          </p>
        </label>
      </div>

      {/* File List */}
      {files.length > 0 && (
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-2">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold">Selected Files ({files.length})</h3>
                <Button onClick={handleUpload} disabled={uploading}>
                  {uploading ? "Uploading..." : "Upload All"}
                </Button>
              </div>
              {files.map((file, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 border rounded-lg"
                >
                  <div className="flex items-center space-x-3 flex-1">
                    <FileText className="h-5 w-5 text-blue-600" />
                    <div className="flex-1">
                      <p className="font-medium text-sm">{file.name}</p>
                      <p className="text-xs text-gray-500">
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    {uploadStatus[file.name] === "success" && (
                      <CheckCircle className="h-5 w-5 text-green-600" />
                    )}
                    {uploadStatus[file.name] === "error" && (
                      <AlertCircle className="h-5 w-5 text-red-600" />
                    )}
                    {!uploading && (
                      <button
                        onClick={() => removeFile(index)}
                        className="text-gray-400 hover:text-red-600"
                      >
                        <X className="h-5 w-5" />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
