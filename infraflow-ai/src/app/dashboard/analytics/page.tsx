"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart3, TrendingUp, DollarSign, Globe } from "lucide-react";

export default function AnalyticsPage() {
  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">Portfolio Analytics</h1>
        <p className="text-gray-600">Comprehensive insights into your infrastructure portfolio</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Portfolio Value</CardTitle>
            <DollarSign className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$2.4B</div>
            <p className="text-xs text-green-600 mt-1">+18.2% vs last quarter</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Active Projects</CardTitle>
            <BarChart3 className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
            <p className="text-xs text-green-600 mt-1">+2 from last month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Countries</CardTitle>
            <Globe className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">8</div>
            <p className="text-xs text-gray-500 mt-1">Across MENA & Africa</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Avg ROI</CardTitle>
            <TrendingUp className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">14.3%</div>
            <p className="text-xs text-green-600 mt-1">Above target</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sector Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Portfolio by Sector</CardTitle>
            <CardDescription>Distribution of investments across sectors</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { name: "Green Hydrogen", value: 35, amount: "$840M" },
                { name: "Solar Energy", value: 28, amount: "$672M" },
                { name: "Wind Energy", value: 22, amount: "$528M" },
                { name: "Hydro Power", value: 10, amount: "$240M" },
                { name: "Other", value: 5, amount: "$120M" },
              ].map((sector, i) => (
                <div key={i}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium">{sector.name}</span>
                    <span className="text-sm text-gray-600">{sector.value}% ({sector.amount})</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="h-2 rounded-full bg-blue-600"
                      style={{ width: `${sector.value}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Geographic Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Portfolio by Country</CardTitle>
            <CardDescription>Geographic distribution of projects</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { name: "Egypt", value: 32, projects: 4 },
                { name: "Morocco", value: 24, projects: 3 },
                { name: "Kenya", value: 18, projects: 2 },
                { name: "South Africa", value: 15, projects: 2 },
                { name: "Tunisia", value: 11, projects: 1 },
              ].map((country, i) => (
                <div key={i}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium">{country.name}</span>
                    <span className="text-sm text-gray-600">{country.value}% ({country.projects} projects)</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="h-2 rounded-full bg-green-600"
                      style={{ width: `${country.value}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Risk Profile */}
        <Card>
          <CardHeader>
            <CardTitle>Portfolio Risk Profile</CardTitle>
            <CardDescription>Aggregate risk assessment</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { category: "Political Risk", score: 6.8, color: "bg-orange-500" },
                { category: "Financial Risk", score: 5.2, color: "bg-yellow-500" },
                { category: "Technical Risk", score: 4.9, color: "bg-green-500" },
                { category: "Environmental Risk", score: 5.5, color: "bg-yellow-500" },
                { category: "Regulatory Risk", score: 6.2, color: "bg-orange-500" },
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

        {/* Financial Performance */}
        <Card>
          <CardHeader>
            <CardTitle>Financial Performance Trend</CardTitle>
            <CardDescription>Quarterly portfolio value growth</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {[
                { quarter: "Q1 2024", value: "$1.8B", growth: "+12%" },
                { quarter: "Q2 2024", value: "$2.0B", growth: "+11%" },
                { quarter: "Q3 2024", value: "$2.2B", growth: "+10%" },
                { quarter: "Q4 2024", value: "$2.4B", growth: "+9%" },
              ].map((period, i) => (
                <div key={i} className="flex items-center justify-between py-2 border-b last:border-0">
                  <span className="font-medium">{period.quarter}</span>
                  <div className="text-right">
                    <p className="font-semibold">{period.value}</p>
                    <p className="text-xs text-green-600">{period.growth}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* DFI Partnerships */}
      <Card>
        <CardHeader>
          <CardTitle>DFI Partnership Performance</CardTitle>
          <CardDescription>Collaboration metrics with Development Finance Institutions</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[
              { name: "EBRD", projects: 5, value: "$980M", avgDuration: "18 months" },
              { name: "EIB", projects: 4, value: "$720M", avgDuration: "16 months" },
              { name: "AfDB", projects: 3, value: "$540M", avgDuration: "20 months" },
              { name: "BII", projects: 2, value: "$360M", avgDuration: "14 months" },
            ].map((dfi, i) => (
              <div key={i} className="p-4 border rounded-lg">
                <h3 className="font-bold text-lg mb-3">{dfi.name}</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-500">Projects:</span>
                    <span className="font-medium">{dfi.projects}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Value:</span>
                    <span className="font-medium">{dfi.value}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Avg Duration:</span>
                    <span className="font-medium">{dfi.avgDuration}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
