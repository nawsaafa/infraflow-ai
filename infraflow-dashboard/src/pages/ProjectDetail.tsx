import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { DashboardLayout } from '@/components/DashboardLayout';
import { Project } from '@/types/project';
import { projectQueries } from '@/lib/supabase';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card } from '@/components/ui/card';
import { 
  ArrowLeft, 
  MapPin, 
  DollarSign, 
  Building2, 
  Calendar,
  TrendingUp,
  AlertTriangle,
  FileCheck,
  File
} from 'lucide-react';

const ProjectDetail = () => {
  const { id } = useParams<{ id: string }>();
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      loadProject(id);
    }
  }, [id]);

  const loadProject = async (projectId: string) => {
    try {
      const data = await projectQueries.getById(projectId);
      setProject(data);
    } catch (error) {
      console.error('Error loading project:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount: number, currency: string) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency || 'USD',
      maximumFractionDigits: 0,
    }).format(amount);
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="text-center py-12">Loading project...</div>
      </DashboardLayout>
    );
  }

  if (!project) {
    return (
      <DashboardLayout>
        <div className="text-center py-12">
          <h2 className="text-xl font-semibold mb-2">Project not found</h2>
          <Link to="/projects">
            <Button variant="outline">← Back to Projects</Button>
          </Link>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <Link to="/projects">
            <Button variant="ghost" className="mb-4 gap-2">
              <ArrowLeft className="h-4 w-4" />
              Back to Projects
            </Button>
          </Link>

          <div className="flex flex-col sm:flex-row justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold mb-2">{project.name}</h1>
              <div className="flex flex-wrap gap-2">
                <Badge className="capitalize">{project.status}</Badge>
                <Badge variant="outline">{project.sector}</Badge>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card className="p-4">
            <div className="flex items-center gap-3">
              <MapPin className="h-5 w-5 text-primary" />
              <div>
                <p className="text-xs text-muted-foreground">Country</p>
                <p className="font-semibold">{project.country}</p>
              </div>
            </div>
          </Card>

          <Card className="p-4">
            <div className="flex items-center gap-3">
              <DollarSign className="h-5 w-5 text-success" />
              <div>
                <p className="text-xs text-muted-foreground">Investment</p>
                <p className="font-semibold">
                  {formatCurrency(project.investment_amount, project.currency)}
                </p>
              </div>
            </div>
          </Card>

          <Card className="p-4">
            <div className="flex items-center gap-3">
              <Building2 className="h-5 w-5 text-primary" />
              <div>
                <p className="text-xs text-muted-foreground">DFI Partners</p>
                <p className="font-semibold">
                  {project.dfi_partners?.length || 0}
                </p>
              </div>
            </div>
          </Card>

          <Card className="p-4">
            <div className="flex items-center gap-3">
              <TrendingUp className="h-5 w-5 text-warning" />
              <div>
                <p className="text-xs text-muted-foreground">Risk Score</p>
                <p className="font-semibold">
                  {project.risk_score ? `${project.risk_score}/10` : 'N/A'}
                </p>
              </div>
            </div>
          </Card>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="financials">Financials</TabsTrigger>
            <TabsTrigger value="risk">Risk</TabsTrigger>
            <TabsTrigger value="compliance">Compliance</TabsTrigger>
            <TabsTrigger value="documents">Documents</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-4">
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4">Project Description</h3>
              <p className="text-muted-foreground">
                {project.description || 'No description available.'}
              </p>
            </Card>

            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4">Key Details</h3>
              <dl className="space-y-3">
                <div className="flex justify-between">
                  <dt className="text-muted-foreground">Created</dt>
                  <dd className="font-medium">
                    {new Date(project.created_at).toLocaleDateString()}
                  </dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-muted-foreground">Last Updated</dt>
                  <dd className="font-medium">
                    {new Date(project.updated_at).toLocaleDateString()}
                  </dd>
                </div>
                {project.expected_completion && (
                  <div className="flex justify-between">
                    <dt className="text-muted-foreground">Expected Completion</dt>
                    <dd className="font-medium">{project.expected_completion}</dd>
                  </div>
                )}
              </dl>
            </Card>
          </TabsContent>

          <TabsContent value="financials">
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <DollarSign className="h-5 w-5" />
                Financial Overview
              </h3>
              <p className="text-muted-foreground">
                Financial analysis module - coming soon
              </p>
            </Card>
          </TabsContent>

          <TabsContent value="risk">
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                Risk Assessment
              </h3>
              <p className="text-muted-foreground">
                Risk analysis module - coming soon
              </p>
            </Card>
          </TabsContent>

          <TabsContent value="compliance">
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <FileCheck className="h-5 w-5" />
                Compliance Check
              </h3>
              <p className="text-muted-foreground">
                Compliance verification module - coming soon
              </p>
            </Card>
          </TabsContent>

          <TabsContent value="documents">
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <File className="h-5 w-5" />
                Project Documents
              </h3>
              <p className="text-muted-foreground">
                Document management module - coming soon
              </p>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  );
};

export default ProjectDetail;
