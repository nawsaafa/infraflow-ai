"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart3, TrendingUp, AlertTriangle, CheckCircle } from "lucide-react";

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Portfolio Overview</h1>
        <p className="text-gray-600">Monitor your infrastructure finance portfolio at a glance</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Active Projects</CardTitle>
            <BarChart3 className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
            <p className="text-xs text-gray-500 mt-1">+2 from last month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total Portfolio Value</CardTitle>
            <TrendingUp className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$2.4B</div>
            <p className="text-xs text-gray-500 mt-1">+18% from last quarter</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Avg Risk Score</CardTitle>
            <AlertTriangle className="h-4 w-4 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">6.2/10</div>
            <p className="text-xs text-gray-500 mt-1">Medium risk profile</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Compliance Rate</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">94%</div>
            <p className="text-xs text-gray-500 mt-1">Above industry average</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Projects */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Projects</CardTitle>
            <CardDescription>Latest infrastructure finance projects</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { name: "Egypt Green Hydrogen", country: "Egypt", value: "$850M", status: "Active" },
                { name: "Kenya Solar Farm", country: "Kenya", value: "$320M", status: "Pending" },
                { name: "Morocco Wind Park", country: "Morocco", value: "$450M", status: "Active" },
              ].map((project, i) => (
                <div key={i} className="flex items-center justify-between py-2 border-b last:border-0">
                  <div>
                    <p className="font-medium">{project.name}</p>
                    <p className="text-sm text-gray-500">{project.country}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold">{project.value}</p>
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      project.status === "Active" ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"
                    }`}>
                      {project.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Risk Analytics */}
        <Card>
          <CardHeader>
            <CardTitle>Risk Analytics</CardTitle>
            <CardDescription>Portfolio risk breakdown</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { category: "Political Risk", score: 7.2, color: "bg-red-500" },
                { category: "Financial Risk", score: 5.8, color: "bg-yellow-500" },
                { category: "Technical Risk", score: 4.5, color: "bg-green-500" },
                { category: "Environmental Risk", score: 6.1, color: "bg-orange-500" },
              ].map((risk, i) => (
                <div key={i}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium">{risk.category}</span>
                    <span className="text-sm text-gray-600">{risk.score}/10</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${risk.color}`}
                      style={{ width: `${risk.score * 10}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Document Processing Status */}
        <Card>
          <CardHeader>
            <CardTitle>Document Processing</CardTitle>
            <CardDescription>Current processing status</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm">Processed</span>
                <span className="font-semibold">847 documents</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">In Queue</span>
                <span className="font-semibold">23 documents</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Failed</span>
                <span className="font-semibold text-red-600">2 documents</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>Common tasks and workflows</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <button className="w-full text-left px-4 py-3 rounded-lg border hover:bg-gray-50 transition-colors">
                <p className="font-medium">Create New Project</p>
                <p className="text-sm text-gray-500">Start a new infrastructure project</p>
              </button>
              <button className="w-full text-left px-4 py-3 rounded-lg border hover:bg-gray-50 transition-colors">
                <p className="font-medium">Upload Documents</p>
                <p className="text-sm text-gray-500">Process new project documents</p>
              </button>
              <button className="w-full text-left px-4 py-3 rounded-lg border hover:bg-gray-50 transition-colors">
                <p className="font-medium">Generate Report</p>
                <p className="text-sm text-gray-500">Create compliance or investment memo</p>
              </button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
