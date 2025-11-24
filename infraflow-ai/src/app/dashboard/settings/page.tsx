"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function SettingsPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Settings</h1>
        <p className="text-gray-600">Manage your platform preferences and integrations</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Account Settings</CardTitle>
            <CardDescription>Manage your account preferences</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Organization Name</label>
              <input
                type="text"
                className="w-full px-3 py-2 border rounded-lg"
                placeholder="Your Organization"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Email</label>
              <input
                type="email"
                className="w-full px-3 py-2 border rounded-lg"
                placeholder="user@example.com"
              />
            </div>
            <Button>Save Changes</Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>API Configuration</CardTitle>
            <CardDescription>Configure backend API settings</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">API Endpoint</label>
              <input
                type="text"
                className="w-full px-3 py-2 border rounded-lg"
                placeholder="http://localhost:8000"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">API Key</label>
              <input
                type="password"
                className="w-full px-3 py-2 border rounded-lg"
                placeholder="Enter API key"
              />
            </div>
            <Button>Update API Settings</Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>DFI Integrations</CardTitle>
            <CardDescription>Connect with DFI platforms</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {["EBRD Portal", "EIB Projects", "AfDB Gateway"].map((dfi) => (
                <div key={dfi} className="flex items-center justify-between p-3 border rounded-lg">
                  <span className="font-medium">{dfi}</span>
                  <Button variant="outline" size="sm">Connect</Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Notifications</CardTitle>
            <CardDescription>Configure alert preferences</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {[
              "Document processing complete",
              "Compliance check results",
              "New project updates",
              "Risk alerts",
            ].map((notif) => (
              <div key={notif} className="flex items-center justify-between">
                <span className="text-sm">{notif}</span>
                <input type="checkbox" defaultChecked className="h-4 w-4" />
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
