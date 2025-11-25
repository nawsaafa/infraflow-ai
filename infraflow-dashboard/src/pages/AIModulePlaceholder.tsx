import { DashboardLayout } from '@/components/DashboardLayout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { LucideIcon } from 'lucide-react';

interface AIModulePlaceholderProps {
  title: string;
  description: string;
  icon: LucideIcon;
  features: string[];
  comingSoon?: boolean;
}

export const AIModulePlaceholder = ({
  title,
  description,
  icon: Icon,
  features,
  comingSoon = true,
}: AIModulePlaceholderProps) => {
  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-4">
            <Icon className="h-8 w-8 text-primary" />
          </div>
          <h1 className="text-3xl font-bold mb-2">{title}</h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            {description}
          </p>
          {comingSoon && (
            <Badge variant="outline" className="mt-4">
              Coming Soon
            </Badge>
          )}
        </div>

        <Card className="p-8">
          <h2 className="text-xl font-semibold mb-4">Planned Features</h2>
          <ul className="space-y-3">
            {features.map((feature, index) => (
              <li key={index} className="flex items-start gap-3">
                <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-primary/10 text-primary text-sm font-medium mt-0.5">
                  {index + 1}
                </span>
                <span className="text-muted-foreground">{feature}</span>
              </li>
            ))}
          </ul>
        </Card>

        <Card className="p-6 bg-accent/50">
          <h3 className="font-semibold mb-2">Integration Ready</h3>
          <p className="text-sm text-muted-foreground mb-4">
            This module will integrate with your existing Supabase database and Pinecone vector store.
            Backend endpoints are already configured and ready for frontend implementation.
          </p>
          <Button disabled>
            Module Under Development
          </Button>
        </Card>
      </div>
    </DashboardLayout>
  );
};
