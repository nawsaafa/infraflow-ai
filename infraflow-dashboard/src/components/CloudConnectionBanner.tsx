import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Cloud, AlertCircle } from 'lucide-react';

export const CloudConnectionBanner = () => {
  return (
    <Alert className="border-warning bg-warning/10">
      <AlertCircle className="h-4 w-4 text-warning" />
      <AlertTitle className="text-warning">Backend Not Connected</AlertTitle>
      <AlertDescription className="mt-2">
        <p className="text-sm text-muted-foreground mb-3">
          Connect Lovable Cloud to access your Supabase database and start displaying infrastructure projects from your backend.
        </p>
        <div className="flex gap-2">
          <Button size="sm" className="gap-2">
            <Cloud className="h-4 w-4" />
            Connect Lovable Cloud
          </Button>
          <Button size="sm" variant="outline" asChild>
            <a href="https://docs.lovable.dev/features/cloud" target="_blank" rel="noopener noreferrer">
              Learn More
            </a>
          </Button>
        </div>
      </AlertDescription>
    </Alert>
  );
};
