import { LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface KPICardProps {
  title: string;
  value: string | number;
  change?: number;
  icon: LucideIcon;
  variant?: 'default' | 'success' | 'warning' | 'destructive';
  description?: string;
}

export const KPICard = ({ 
  title, 
  value, 
  change, 
  icon: Icon, 
  variant = 'default',
  description 
}: KPICardProps) => {
  const variants = {
    default: 'bg-primary/10 text-primary',
    success: 'bg-success/10 text-success',
    warning: 'bg-warning/10 text-warning',
    destructive: 'bg-destructive/10 text-destructive',
  };

  return (
    <div className="kpi-card group">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-muted-foreground">{title}</p>
          <h3 className="text-3xl font-bold mt-2">{value}</h3>
          {description && (
            <p className="text-xs text-muted-foreground mt-1">{description}</p>
          )}
          {change !== undefined && (
            <div className="flex items-center mt-2">
              <span className={cn(
                "text-sm font-medium",
                change > 0 ? "text-success" : "text-destructive"
              )}>
                {change > 0 ? '+' : ''}{change}%
              </span>
              <span className="text-xs text-muted-foreground ml-2">vs last month</span>
            </div>
          )}
        </div>
        <div className={cn(
          "p-3 rounded-lg transition-transform group-hover:scale-110",
          variants[variant]
        )}>
          <Icon className="h-6 w-6" />
        </div>
      </div>
    </div>
  );
};
