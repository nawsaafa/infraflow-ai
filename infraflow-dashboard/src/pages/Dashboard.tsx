import { useEffect, useState } from 'react';
import { DashboardLayout } from '@/components/DashboardLayout';
import { KPICard } from '@/components/KPICard';
import { ProjectCard } from '@/components/ProjectCard';
import { CloudConnectionBanner } from '@/components/CloudConnectionBanner';
import { DollarSign, FolderKanban, Globe, Building2, TrendingUp, Clock } from 'lucide-react';
import { Project, DashboardKPIs, PipelineData } from '@/types/project';
import { projectQueries, isSupabaseConfigured } from '@/lib/supabase';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

const Dashboard = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [kpis, setKpis] = useState<DashboardKPIs | null>(null);
  const [pipeline, setPipeline] = useState<PipelineData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const allProjects = await projectQueries.getAll();
      setProjects(allProjects || []);

      // Calculate KPIs
      if (allProjects) {
        const totalInvestment = allProjects.reduce((sum, p) => sum + (p.investment_amount || 0), 0);
        const uniqueCountries = new Set(allProjects.map(p => p.country)).size;
        const uniqueDFIs = new Set(
          allProjects.flatMap(p => p.dfi_partners || [])
        ).size;
        const activeCount = allProjects.filter(p => p.status === 'active').length;

        setKpis({
          total_projects: allProjects.length,
          total_investment: totalInvestment,
          active_projects: activeCount,
          countries_count: uniqueCountries,
          dfi_partners_count: uniqueDFIs,
        });

        // Calculate pipeline
        const statuses = ['draft', 'active', 'analyzed', 'completed'] as const;
        const pipelineData = statuses.map(status => ({
          status,
          count: allProjects.filter(p => p.status === status).length,
          value: allProjects
            .filter(p => p.status === status)
            .reduce((sum, p) => sum + (p.investment_amount || 0), 0),
        }));
        setPipeline(pipelineData);
      }
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      notation: 'compact',
      maximumFractionDigits: 1,
    }).format(amount);
  };

  const recentProjects = projects.slice(0, 5);

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Connection Banner */}
        {!isSupabaseConfigured && <CloudConnectionBanner />}
        
        {/* KPIs */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <KPICard
            title="Total Projects"
            value={kpis?.total_projects || 0}
            icon={FolderKanban}
            variant="default"
          />
          <KPICard
            title="Total Investment"
            value={formatCurrency(kpis?.total_investment || 0)}
            icon={DollarSign}
            variant="success"
          />
          <KPICard
            title="Countries"
            value={kpis?.countries_count || 0}
            icon={Globe}
            variant="default"
          />
          <KPICard
            title="DFI Partners"
            value={kpis?.dfi_partners_count || 0}
            icon={Building2}
            variant="default"
          />
        </div>

        {/* Pipeline View */}
        <Card className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold">Project Pipeline</h2>
            <TrendingUp className="h-5 w-5 text-muted-foreground" />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {pipeline.map((stage) => (
              <div key={stage.status} className="kpi-card">
                <div className="flex items-center justify-between mb-2">
                  <Badge variant="outline" className="capitalize">
                    {stage.status}
                  </Badge>
                  <span className="text-2xl font-bold">{stage.count}</span>
                </div>
                <p className="text-sm text-muted-foreground">
                  {formatCurrency(stage.value)}
                </p>
              </div>
            ))}
          </div>
        </Card>

        {/* Recent Activity */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Clock className="h-5 w-5" />
              Recent Projects
            </h2>
            <a 
              href="/projects" 
              className="text-sm text-primary hover:underline font-medium"
            >
              View all →
            </a>
          </div>

          {loading ? (
            <div className="text-center py-12 text-muted-foreground">
              Loading projects...
            </div>
          ) : recentProjects.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {recentProjects.map((project) => (
                <ProjectCard key={project.id} project={project} />
              ))}
            </div>
          ) : (
            <Card className="p-12 text-center">
              <FolderKanban className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
              <h3 className="text-lg font-semibold mb-2">No projects yet</h3>
              <p className="text-muted-foreground">
                Connect to Lovable Cloud to start tracking infrastructure projects
              </p>
            </Card>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Dashboard;
