"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Shield, CheckCircle, AlertTriangle, XCircle, RefreshCw } from "lucide-react";

export default function CompliancePage() {
  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Compliance Monitoring</h1>
          <p className="text-gray-600">Track regulatory and standards compliance across your portfolio</p>
        </div>
        <Button>
          <RefreshCw className="mr-2 h-4 w-4" />
          Run Compliance Check
        </Button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Compliance Rate</CardTitle>
            <Shield className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">94%</div>
            <p className="text-xs text-gray-500 mt-1">Above industry average</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Compliant Projects</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">11</div>
            <p className="text-xs text-gray-500 mt-1">Out of 12 projects</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Pending Reviews</CardTitle>
            <AlertTriangle className="h-4 w-4 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-600">3</div>
            <p className="text-xs text-gray-500 mt-1">Require attention</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Issues Found</CardTitle>
            <XCircle className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">5</div>
            <p className="text-xs text-gray-500 mt-1">Across 2 projects</p>
          </CardContent>
        </Card>
      </div>

      {/* Standards Compliance */}
      <Card>
        <CardHeader>
          <CardTitle>Standards Compliance Overview</CardTitle>
          <CardDescription>Compliance status across major standards and frameworks</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {[
              {
                name: "EBRD Environmental Standards",
                compliant: 11,
                total: 12,
                issues: ["Minor documentation gap in 1 project"],
              },
              {
                name: "IFC Performance Standards",
                compliant: 12,
                total: 12,
                issues: [],
              },
              {
                name: "EU Taxonomy Alignment",
                compliant: 10,
                total: 12,
                issues: ["2 projects pending classification", "Revenue alignment calculation needed"],
              },
              {
                name: "Local Content Requirements",
                compliant: 11,
                total: 12,
                issues: ["1 project below threshold"],
              },
              {
                name: "ESG Reporting Framework",
                compliant: 12,
                total: 12,
                issues: [],
              },
            ].map((standard, i) => (
              <div key={i} className="border rounded-lg p-4">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-semibold text-lg">{standard.name}</h3>
                    <p className="text-sm text-gray-500 mt-1">
                      {standard.compliant} of {standard.total} projects compliant
                    </p>
                  </div>
                  {standard.compliant === standard.total ? (
                    <CheckCircle className="h-6 w-6 text-green-500" />
                  ) : (
                    <AlertTriangle className="h-6 w-6 text-yellow-500" />
                  )}
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mb-3">
                  <div
                    className={`h-2 rounded-full ${
                      standard.compliant === standard.total ? "bg-green-500" : "bg-yellow-500"
                    }`}
                    style={{ width: `${(standard.compliant / standard.total) * 100}%` }}
                  />
                </div>
                {standard.issues.length > 0 && (
                  <div className="mt-3 pt-3 border-t">
                    <p className="text-sm font-medium text-gray-700 mb-2">Issues:</p>
                    <ul className="space-y-1">
                      {standard.issues.map((issue, j) => (
                        <li key={j} className="text-sm text-red-600 flex items-start">
                          <span className="mr-2">•</span>
                          <span>{issue}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Project-Level Compliance */}
      <Card>
        <CardHeader>
          <CardTitle>Project Compliance Status</CardTitle>
          <CardDescription>Detailed compliance view by project</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[
              {
                project: "Egypt Green Hydrogen",
                standards: { EBRD: "compliant", IFC: "compliant", EU: "pending", ESG: "compliant" },
                overallScore: 92,
              },
              {
                project: "Kenya Solar Farm",
                standards: { EBRD: "compliant", IFC: "compliant", EU: "compliant", ESG: "compliant" },
                overallScore: 100,
              },
              {
                project: "Morocco Wind Park",
                standards: { EBRD: "compliant", IFC: "compliant", EU: "non-compliant", ESG: "compliant" },
                overallScore: 85,
              },
            ].map((project, i) => (
              <div key={i} className="border rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <div>
                    <h3 className="font-semibold">{project.project}</h3>
                    <p className="text-sm text-gray-500">Overall Compliance: {project.overallScore}%</p>
                  </div>
                  <Button variant="outline" size="sm">View Details</Button>
                </div>
                <div className="grid grid-cols-4 gap-2">
                  {Object.entries(project.standards).map(([standard, status]) => (
                    <div
                      key={standard}
                      className={`px-3 py-2 rounded text-center text-xs font-medium ${
                        status === "compliant"
                          ? "bg-green-100 text-green-800"
                          : status === "pending"
                          ? "bg-yellow-100 text-yellow-800"
                          : "bg-red-100 text-red-800"
                      }`}
                    >
                      {standard}: {status}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Recent Compliance Checks */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Compliance Checks</CardTitle>
          <CardDescription>Latest automated compliance assessments</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[
              { date: "2024-01-20", project: "Egypt Green Hydrogen", standard: "EBRD Standards", result: "Passed", issues: 0 },
              { date: "2024-01-19", project: "Kenya Solar Farm", standard: "IFC Performance", result: "Passed", issues: 0 },
              { date: "2024-01-18", project: "Morocco Wind Park", standard: "EU Taxonomy", result: "Failed", issues: 2 },
              { date: "2024-01-17", project: "Tunisia Solar", standard: "Local Content", result: "Passed", issues: 0 },
            ].map((check, i) => (
              <div key={i} className="flex items-center justify-between py-3 border-b last:border-0">
                <div className="flex-1">
                  <p className="font-medium">{check.project}</p>
                  <p className="text-sm text-gray-500">{check.standard}</p>
                </div>
                <div className="flex items-center space-x-4">
                  <p className="text-sm text-gray-500">{check.date}</p>
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-medium ${
                      check.result === "Passed"
                        ? "bg-green-100 text-green-800"
                        : "bg-red-100 text-red-800"
                    }`}
                  >
                    {check.result}
                  </span>
                  {check.issues > 0 && (
                    <span className="text-sm text-red-600">{check.issues} issues</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
