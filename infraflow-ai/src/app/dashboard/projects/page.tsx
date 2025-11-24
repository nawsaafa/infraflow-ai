"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Plus, Search, Filter } from "lucide-react";

const mockProjects = [
  {
    id: "1",
    name: "Egypt Green Hydrogen Project",
    sponsor: "ACWA Power",
    country: "Egypt",
    sector: "Green Hydrogen",
    total_value: 850000000,
    status: "active",
    risk_score: 6.5,
    dfi_partners: ["EBRD", "EIB"],
  },
  {
    id: "2",
    name: "Kenya Solar Farm",
    sponsor: "SolarTech Africa",
    country: "Kenya",
    sector: "Solar Energy",
    total_value: 320000000,
    status: "pending",
    risk_score: 5.2,
    dfi_partners: ["AfDB"],
  },
  {
    id: "3",
    name: "Morocco Wind Park",
    sponsor: "WindPower Med",
    country: "Morocco",
    sector: "Wind Energy",
    total_value: 450000000,
    status: "active",
    risk_score: 4.8,
    dfi_partners: ["EIB", "BII"],
  },
];

export default function ProjectsPage() {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredProjects = mockProjects.filter(project =>
    project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    project.country.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Projects</h1>
          <p className="text-gray-600">Manage your infrastructure finance portfolio</p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          New Project
        </Button>
      </div>

      {/* Search and Filters */}
      <div className="flex items-center gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search projects..."
            className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <Button variant="outline">
          <Filter className="mr-2 h-4 w-4" />
          Filters
        </Button>
      </div>

      {/* Projects Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredProjects.map((project) => (
          <Link key={project.id} href={`/dashboard/projects/${project.id}`}>
            <Card className="hover:shadow-lg transition-shadow cursor-pointer h-full">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <CardTitle className="text-lg">{project.name}</CardTitle>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    project.status === "active"
                      ? "bg-green-100 text-green-800"
                      : "bg-yellow-100 text-yellow-800"
                  }`}>
                    {project.status}
                  </span>
                </div>
                <CardDescription>{project.sponsor}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-500">Country:</span>
                    <span className="font-medium">{project.country}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Sector:</span>
                    <span className="font-medium">{project.sector}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Value:</span>
                    <span className="font-medium">
                      ${(project.total_value / 1000000).toFixed(0)}M
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Risk Score:</span>
                    <span className={`font-medium ${
                      project.risk_score > 7 ? "text-red-600" :
                      project.risk_score > 5 ? "text-yellow-600" : "text-green-600"
                    }`}>
                      {project.risk_score}/10
                    </span>
                  </div>
                  <div className="pt-2 border-t">
                    <p className="text-gray-500 mb-2">DFI Partners:</p>
                    <div className="flex flex-wrap gap-1">
                      {project.dfi_partners.map((dfi) => (
                        <span
                          key={dfi}
                          className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded"
                        >
                          {dfi}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>

      {/* Empty State */}
      {filteredProjects.length === 0 && (
        <Card className="py-12">
          <CardContent className="text-center">
            <p className="text-gray-500">No projects found matching your search.</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
