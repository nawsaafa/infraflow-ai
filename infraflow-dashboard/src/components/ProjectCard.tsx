import { Link } from 'react-router-dom';
import { Badge } from '@/components/ui/badge';
import { Project } from '@/types/project';
import { MapPin, DollarSign, Building2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ProjectCardProps {
  project: Project;
}

const statusColors = {
  draft: 'bg-muted text-muted-foreground',
  active: 'bg-primary/10 text-primary',
  analyzed: 'bg-warning/10 text-warning',
  completed: 'bg-success/10 text-success',
};

const sectorIcons = {
  energy: '⚡',
  transport: '🚆',
  water: '💧',
  telecom: '📡',
  social: '🏥',
};

export const ProjectCard = ({ project }: ProjectCardProps) => {
  const formatCurrency = (amount: number, currency: string) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency || 'USD',
      notation: 'compact',
      maximumFractionDigits: 1,
    }).format(amount);
  };

  return (
    <Link to={`/projects/${project.id}`}>
      <div className="kpi-card group cursor-pointer">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-2">
            <span className="text-2xl">{sectorIcons[project.sector]}</span>
            <Badge className={cn(statusColors[project.status])}>
              {project.status}
            </Badge>
          </div>
          {project.risk_score && (
            <Badge variant="outline" className="text-xs">
              Risk: {project.risk_score}/10
            </Badge>
          )}
        </div>

        <h3 className="text-lg font-semibold mb-2 group-hover:text-primary transition-colors">
          {project.name}
        </h3>

        <div className="space-y-2 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <MapPin className="h-4 w-4" />
            <span>{project.country}</span>
          </div>
          
          <div className="flex items-center gap-2">
            <DollarSign className="h-4 w-4" />
            <span className="font-semibold text-foreground">
              {formatCurrency(project.investment_amount, project.currency)}
            </span>
          </div>

          {project.dfi_partners && project.dfi_partners.length > 0 && (
            <div className="flex items-center gap-2">
              <Building2 className="h-4 w-4" />
              <span>{project.dfi_partners.length} DFI Partners</span>
            </div>
          )}
        </div>

        {project.description && (
          <p className="text-sm text-muted-foreground mt-3 line-clamp-2">
            {project.description}
          </p>
        )}
      </div>
    </Link>
  );
};
