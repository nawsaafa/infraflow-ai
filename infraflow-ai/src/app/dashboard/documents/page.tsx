"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileUpload } from "@/components/dashboard/file-upload";
import { FileText, Filter, Download, Eye, Trash2 } from "lucide-react";

const mockDocuments = [
  {
    id: "1",
    name: "Project Feasibility Study.pdf",
    project: "Egypt Green Hydrogen",
    type: "Feasibility Study",
    uploaded: "2024-01-15",
    processed: true,
    size: "12.5 MB",
  },
  {
    id: "2",
    name: "Environmental Impact Assessment.pdf",
    project: "Egypt Green Hydrogen",
    type: "EIA Report",
    uploaded: "2024-01-16",
    processed: true,
    size: "8.2 MB",
  },
  {
    id: "3",
    name: "Financial Model.xlsx",
    project: "Kenya Solar Farm",
    type: "Financial Model",
    uploaded: "2024-01-18",
    processed: false,
    size: "3.1 MB",
  },
];

export default function DocumentsPage() {
  const [showUpload, setShowUpload] = useState(false);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Document Processing Center</h1>
          <p className="text-gray-600">Upload and manage project documents with AI-powered analysis</p>
        </div>
        <Button onClick={() => setShowUpload(!showUpload)}>
          {showUpload ? "View Documents" : "Upload Documents"}
        </Button>
      </div>

      {/* Upload Section */}
      {showUpload && (
        <Card>
          <CardHeader>
            <CardTitle>Upload New Documents</CardTitle>
            <CardDescription>
              Upload project documents for automated processing and analysis
            </CardDescription>
          </CardHeader>
          <CardContent>
            <FileUpload
              onUploadComplete={(files) => {
                console.log("Uploaded files:", files);
                setShowUpload(false);
              }}
            />
          </CardContent>
        </Card>
      )}

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Total Documents</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">847</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Processed</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">822</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">In Queue</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-600">23</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Failed</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">2</div>
          </CardContent>
        </Card>
      </div>

      {/* Documents Table */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Recent Documents</CardTitle>
              <CardDescription>All uploaded project documents</CardDescription>
            </div>
            <Button variant="outline">
              <Filter className="mr-2 h-4 w-4" />
              Filter
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {mockDocuments.map((doc) => (
              <div
                key={doc.id}
                className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50"
              >
                <div className="flex items-center space-x-4 flex-1">
                  <FileText className="h-8 w-8 text-blue-600" />
                  <div className="flex-1">
                    <p className="font-medium">{doc.name}</p>
                    <p className="text-sm text-gray-500">
                      {doc.project} • {doc.type} • {doc.size}
                    </p>
                  </div>
                  <div>
                    <span
                      className={`px-2 py-1 text-xs rounded-full ${
                        doc.processed
                          ? "bg-green-100 text-green-800"
                          : "bg-yellow-100 text-yellow-800"
                      }`}
                    >
                      {doc.processed ? "Processed" : "Processing"}
                    </span>
                  </div>
                  <p className="text-sm text-gray-500">{doc.uploaded}</p>
                </div>
                <div className="flex items-center space-x-2">
                  <Button variant="ghost" size="sm">
                    <Eye className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="sm">
                    <Download className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="sm">
                    <Trash2 className="h-4 w-4 text-red-600" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Processing Pipeline */}
      <Card>
        <CardHeader>
          <CardTitle>AI Processing Pipeline</CardTitle>
          <CardDescription>Automated document analysis workflow</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              { step: "Document Upload", status: "Completed", time: "< 1 min" },
              { step: "OCR & Text Extraction", status: "Completed", time: "2-5 min" },
              { step: "Entity Recognition", status: "In Progress", time: "3-7 min" },
              { step: "Risk Analysis", status: "Pending", time: "5-10 min" },
              { step: "Compliance Check", status: "Pending", time: "5-10 min" },
            ].map((step, i) => (
              <div key={i} className="flex items-center justify-between py-2 border-b last:border-0">
                <div className="flex items-center space-x-4">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    step.status === "Completed"
                      ? "bg-green-100 text-green-800"
                      : step.status === "In Progress"
                      ? "bg-blue-100 text-blue-800"
                      : "bg-gray-100 text-gray-800"
                  }`}>
                    {i + 1}
                  </div>
                  <div>
                    <p className="font-medium">{step.step}</p>
                    <p className="text-sm text-gray-500">Avg. processing time: {step.time}</p>
                  </div>
                </div>
                <span className={`px-2 py-1 text-xs rounded-full ${
                  step.status === "Completed"
                    ? "bg-green-100 text-green-800"
                    : step.status === "In Progress"
                    ? "bg-blue-100 text-blue-800"
                    : "bg-gray-100 text-gray-800"
                }`}>
                  {step.status}
                </span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
