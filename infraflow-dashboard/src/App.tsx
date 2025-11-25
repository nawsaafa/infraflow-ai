import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";
import ProjectDetail from "./pages/ProjectDetail";
import SemanticSearch from "./pages/SemanticSearch";
import Compliance from "./pages/Compliance";
import MemoGenerator from "./pages/MemoGenerator";
import FinancialTools from "./pages/FinancialTools";
import RiskAnalysis from "./pages/RiskAnalysis";
import Portfolio from "./pages/Portfolio";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/projects/:id" element={<ProjectDetail />} />
          <Route path="/search" element={<SemanticSearch />} />
          <Route path="/compliance" element={<Compliance />} />
          <Route path="/memo" element={<MemoGenerator />} />
          <Route path="/financial" element={<FinancialTools />} />
          <Route path="/risk" element={<RiskAnalysis />} />
          <Route path="/portfolio" element={<Portfolio />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
