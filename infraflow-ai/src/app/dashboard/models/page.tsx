"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Calculator, Download, Plus } from "lucide-react";

export default function ModelsPage() {
  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Financial Models</h1>
          <p className="text-gray-600">DCF models and scenario analysis library</p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          New Model
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Model Library</CardTitle>
          <CardDescription>Financial models and projections</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              { name: "Egypt Green Hydrogen - Base Case", project: "Egypt Green Hydrogen", scenarios: 3, lastUpdated: "2024-01-20" },
              { name: "Kenya Solar - Sensitivity Analysis", project: "Kenya Solar Farm", scenarios: 5, lastUpdated: "2024-01-18" },
              { name: "Morocco Wind - Monte Carlo", project: "Morocco Wind Park", scenarios: 10000, lastUpdated: "2024-01-15" },
            ].map((model, i) => (
              <div key={i} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center space-x-4">
                  <Calculator className="h-8 w-8 text-blue-600" />
                  <div>
                    <p className="font-medium">{model.name}</p>
                    <p className="text-sm text-gray-500">{model.project} • {model.scenarios} scenarios</p>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <p className="text-sm text-gray-500">{model.lastUpdated}</p>
                  <Button variant="outline" size="sm">
                    <Download className="mr-2 h-4 w-4" />
                    Export
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
