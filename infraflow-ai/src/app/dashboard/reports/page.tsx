"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileCheck, Download, Plus } from "lucide-react";

export default function ReportsPage() {
  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Generated Reports</h1>
          <p className="text-gray-600">Investment memos and compliance reports</p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Generate Report
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Report Library</CardTitle>
          <CardDescription>All generated reports and documents</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              { name: "Egypt Green Hydrogen - Investment Memo", type: "Investment Memo", date: "2024-01-20", status: "Final" },
              { name: "Kenya Solar - Compliance Report", type: "Compliance", date: "2024-01-19", status: "Draft" },
              { name: "Morocco Wind - Risk Assessment", type: "Risk Analysis", date: "2024-01-18", status: "Final" },
            ].map((report, i) => (
              <div key={i} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center space-x-4">
                  <FileCheck className="h-8 w-8 text-blue-600" />
                  <div>
                    <p className="font-medium">{report.name}</p>
                    <p className="text-sm text-gray-500">{report.type} • {report.date}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    report.status === "Final" ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"
                  }`}>
                    {report.status}
                  </span>
                  <Button variant="outline" size="sm">
                    <Download className="mr-2 h-4 w-4" />
                    Download
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
