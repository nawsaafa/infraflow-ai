"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  FolderKanban,
  FileText,
  BarChart3,
  Shield,
  Calculator,
  FileCheck,
  Settings,
  Zap
} from "lucide-react";

const navigation = [
  { name: "Overview", href: "/dashboard", icon: LayoutDashboard },
  { name: "Projects", href: "/dashboard/projects", icon: FolderKanban },
  { name: "Documents", href: "/dashboard/documents", icon: FileText },
  { name: "Analytics", href: "/dashboard/analytics", icon: BarChart3 },
  { name: "Compliance", href: "/dashboard/compliance", icon: Shield },
  { name: "Models", href: "/dashboard/models", icon: Calculator },
  { name: "Reports", href: "/dashboard/reports", icon: FileCheck },
  { name: "Settings", href: "/dashboard/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex h-screen w-64 flex-col border-r bg-gray-50">
      {/* Logo */}
      <div className="flex h-16 items-center border-b px-6">
        <Link href="/dashboard" className="flex items-center space-x-2">
          <Zap className="h-8 w-8 text-blue-600" />
          <span className="text-xl font-bold">InfraFlow AI</span>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3 py-4">
        {navigation.map((item) => {
          const isActive = pathname === item.href ||
            (item.href !== "/dashboard" && pathname.startsWith(item.href));

          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center space-x-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-blue-600 text-white"
                  : "text-gray-700 hover:bg-gray-100"
              )}
            >
              <item.icon className="h-5 w-5" />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>

      {/* User section */}
      <div className="border-t p-4">
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-semibold">
            U
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium">User Name</p>
            <p className="text-xs text-gray-500">user@example.com</p>
          </div>
        </div>
      </div>
    </div>
  );
}
