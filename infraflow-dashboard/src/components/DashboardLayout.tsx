import { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { 
  LayoutDashboard, 
  FolderKanban, 
  Search, 
  FileCheck, 
  FileText,
  Calculator,
  TrendingUp,
  BarChart3,
  Menu,
  X
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useState } from 'react';

interface DashboardLayoutProps {
  children: ReactNode;
}

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Projects', href: '/projects', icon: FolderKanban },
  { name: 'Semantic Search', href: '/search', icon: Search },
  { name: 'Compliance', href: '/compliance', icon: FileCheck },
  { name: 'Memo Generator', href: '/memo', icon: FileText },
  { name: 'Financial Tools', href: '/financial', icon: Calculator },
  { name: 'Risk Analysis', href: '/risk', icon: TrendingUp },
  { name: 'Portfolio', href: '/portfolio', icon: BarChart3 },
];

export const DashboardLayout = ({ children }: DashboardLayoutProps) => {
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={cn(
        "fixed top-0 left-0 z-50 h-full w-64 bg-sidebar text-sidebar-foreground transform transition-transform duration-200 lg:translate-x-0",
        sidebarOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="p-6 border-b border-sidebar-foreground/10">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-xl font-bold">InfraFlow AI</h1>
                <p className="text-xs text-sidebar-foreground/60 mt-1">
                  Infrastructure Finance Intelligence
                </p>
              </div>
              <Button
                variant="ghost"
                size="icon"
                className="lg:hidden text-sidebar-foreground"
                onClick={() => setSidebarOpen(false)}
              >
                <X className="h-5 w-5" />
              </Button>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={() => setSidebarOpen(false)}
                  className={cn(
                    "flex items-center gap-3 px-3 py-2 rounded-lg transition-colors",
                    isActive
                      ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium"
                      : "text-sidebar-foreground/80 hover:bg-sidebar-foreground/10 hover:text-sidebar-foreground"
                  )}
                >
                  <item.icon className="h-5 w-5" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-sidebar-foreground/10">
            <p className="text-xs text-sidebar-foreground/60">
              © 2025 InfraFlow AI
            </p>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className="lg:pl-64">
        {/* Top bar */}
        <header className="sticky top-0 z-30 bg-background border-b border-border">
          <div className="flex items-center justify-between px-6 py-4">
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu className="h-5 w-5" />
            </Button>
            
            <div className="flex-1 lg:flex-none">
              <h2 className="text-lg font-semibold">
                {navigation.find(n => n.href === location.pathname)?.name || 'InfraFlow AI'}
              </h2>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  );
};
