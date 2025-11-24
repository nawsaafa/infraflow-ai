"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Upload, FileText, BarChart3, Shield, Download } from "lucide-react";
import Link from "next/link";

export default function ProjectDetailPage({ params }: { params: { id: string } }) {
  const [activeTab, setActiveTab] = useState("overview");

  // Mock project data
  const project = {
    id: params.id,
    name: "Egypt Green Hydrogen Project",
    sponsor: "ACWA Power",
    country: "Egypt",
    sector: "Green Hydrogen",
    total_value: 850000000,
    status: "active",
    risk_score: 6.5,
    dfi_partners: ["EBRD", "EIB"],
    description: "Large-scale green hydrogen production facility in Egypt, leveraging renewable energy sources to produce sustainable hydrogen for export and domestic use.",
  };

  const tabs = [
    { id: "overview", label: "Overview", icon: FileText },
    { id: "documents", label: "Documents", icon: FileText },
    { id: "financials", label: "Financials", icon: BarChart3 },
    { id: "compliance", label: "Compliance", icon: Shield },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <Link href="/dashboard/projects">
          <Button variant="ghost" className="mb-4">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Projects
          </Button>
        </Link>
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">{project.name}</h1>
            <p className="text-gray-600">{project.sponsor} • {project.country}</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline">
              <Download className="mr-2 h-4 w-4" />
              Export Report
            </Button>
            <Button>
              <Upload className="mr-2 h-4 w-4" />
              Upload Documents
            </Button>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b">
        <div className="flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 pb-4 border-b-2 transition-colors ${
                activeTab === tab.id
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              <tab.icon className="h-4 w-4" />
              <span>{tab.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === "overview" && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Project Details</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h3 className="font-semibold mb-2">Description</h3>
                    <p className="text-gray-600">{project.description}</p>
                  </div>
                  <div className="grid grid-cols-2 gap-4 pt-4">
                    <div>
                      <p className="text-sm text-gray-500">Sector</p>
                      <p className="font-medium">{project.sector}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Status</p>
                      <span className={`inline-block px-2 py-1 text-xs rounded-full ${
                        project.status === "active"
                          ? "bg-green-100 text-green-800"
                          : "bg-yellow-100 text-yellow-800"
                      }`}>
                        {project.status}
                      </span>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Total Value</p>
                      <p className="font-medium">${(project.total_value / 1000000).toFixed(0)}M</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Risk Score</p>
                      <p className="font-medium">{project.risk_score}/10</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Key Milestones</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { title: "Financial Close", date: "Q2 2024", status: "completed" },
                    { title: "Construction Start", date: "Q3 2024", status: "in-progress" },
                    { title: "First Production", date: "Q4 2025", status: "upcoming" },
                    { title: "Commercial Operation", date: "Q1 2026", status: "upcoming" },
                  ].map((milestone, i) => (
                    <div key={i} className="flex items-center justify-between py-2 border-b last:border-0">
                      <div>
                        <p className="font-medium">{milestone.title}</p>
                        <p className="text-sm text-gray-500">{milestone.date}</p>
                      </div>
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        milestone.status === "completed"
                          ? "bg-green-100 text-green-800"
                          : milestone.status === "in-progress"
                          ? "bg-blue-100 text-blue-800"
                          : "bg-gray-100 text-gray-800"
                      }`}>
                        {milestone.status}
                      </span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>DFI Partners</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {project.dfi_partners.map((dfi) => (
                    <div key={dfi} className="p-3 border rounded-lg">
                      <p className="font-medium">{dfi}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Risk Assessment</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {[
                    { name: "Political Risk", value: 7 },
                    { name: "Financial Risk", value: 6 },
                    { name: "Technical Risk", value: 5 },
                    { name: "Environmental Risk", value: 6 },
                  ].map((risk, i) => (
                    <div key={i}>
                      <div className="flex justify-between mb-1">
                        <span className="text-sm">{risk.name}</span>
                        <span className="text-sm font-medium">{risk.value}/10</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            risk.value > 7
                              ? "bg-red-500"
                              : risk.value > 5
                              ? "bg-yellow-500"
                              : "bg-green-500"
                          }`}
                          style={{ width: `${risk.value * 10}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <Button variant="outline" className="w-full justify-start">
                    <FileText className="mr-2 h-4 w-4" />
                    Generate Investment Memo
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Shield className="mr-2 h-4 w-4" />
                    Run Compliance Check
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <BarChart3 className="mr-2 h-4 w-4" />
                    View Financial Model
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {activeTab === "documents" && (
        <Card>
          <CardHeader>
            <CardTitle>Project Documents</CardTitle>
            <CardDescription>Uploaded and processed documents for this project</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-gray-500 text-center py-8">Document management interface coming soon...</p>
          </CardContent>
        </Card>
      )}

      {activeTab === "financials" && (
        <Card>
          <CardHeader>
            <CardTitle>Financial Analysis</CardTitle>
            <CardDescription>Financial models and projections</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-gray-500 text-center py-8">Financial modeling interface coming soon...</p>
          </CardContent>
        </Card>
      )}

      {activeTab === "compliance" && (
        <Card>
          <CardHeader>
            <CardTitle>Compliance Status</CardTitle>
            <CardDescription>Regulatory and standards compliance</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-gray-500 text-center py-8">Compliance dashboard coming soon...</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
