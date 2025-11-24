import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight, BarChart3, FileCheck, Zap, Shield } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Zap className="h-8 w-8 text-blue-600" />
            <span className="text-2xl font-bold">InfraFlow AI</span>
          </div>
          <nav className="hidden md:flex items-center space-x-6">
            <Link href="#features" className="text-gray-600 hover:text-gray-900">Features</Link>
            <Link href="#solutions" className="text-gray-600 hover:text-gray-900">Solutions</Link>
            <Link href="#case-studies" className="text-gray-600 hover:text-gray-900">Case Studies</Link>
            <Link href="/dashboard" className="text-gray-600 hover:text-gray-900">Dashboard</Link>
          </nav>
          <div className="flex items-center space-x-4">
            <Link href="/dashboard">
              <Button variant="outline">Sign In</Button>
            </Link>
            <Link href="/dashboard">
              <Button>Start Free Pilot</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          Accelerate Energy Transition Financing with AI
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          The intelligent platform connecting $130 trillion in climate finance
          with bankable infrastructure projects.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link href="/dashboard">
            <Button size="lg" className="text-lg px-8">
              Start Free Pilot
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
          <Link href="#demo">
            <Button size="lg" variant="outline" className="text-lg px-8">
              Book Demo
            </Button>
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="container mx-auto px-4 py-20">
        <div className="grid md:grid-cols-2 gap-12 mb-20">
          {/* For DFIs */}
          <div className="space-y-6">
            <h2 className="text-3xl font-bold mb-4">For Development Finance Institutions</h2>
            <div className="space-y-4">
              <FeatureItem icon={<Zap />} text="50% faster due diligence" />
              <FeatureItem icon={<FileCheck />} text="Automated compliance checking" />
              <FeatureItem icon={<BarChart3 />} text="Risk prediction powered by 1000+ projects" />
              <FeatureItem icon={<Shield />} text="One-click investment memos" />
            </div>
          </div>

          {/* For Project Sponsors */}
          <div className="space-y-6">
            <h2 className="text-3xl font-bold mb-4">For Project Sponsors</h2>
            <div className="space-y-4">
              <FeatureItem icon={<FileCheck />} text="DFI-ready documentation" />
              <FeatureItem icon={<BarChart3 />} text="Financial model optimization" />
              <FeatureItem icon={<Shield />} text="Multi-stakeholder coordination" />
              <FeatureItem icon={<Zap />} text="Regulatory navigation" />
            </div>
          </div>
        </div>
      </section>

      {/* Solutions Cards */}
      <section id="solutions" className="container mx-auto px-4 py-20 bg-gray-50">
        <h2 className="text-4xl font-bold text-center mb-12">Comprehensive Infrastructure Finance Solutions</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <Card>
            <CardHeader>
              <FileCheck className="h-12 w-12 text-blue-600 mb-4" />
              <CardTitle>Document Intelligence</CardTitle>
              <CardDescription>
                Multi-language processing of 1000+ page documents with automated key term extraction
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>Auto-generate executive summaries</li>
                <li>Risk factor identification</li>
                <li>Regulatory compliance checking</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <BarChart3 className="h-12 w-12 text-blue-600 mb-4" />
              <CardTitle>Financial Modeling</CardTitle>
              <CardDescription>
                DCF analysis with 10,000 scenarios and blended finance structuring
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>Currency risk modeling</li>
                <li>Political risk quantification</li>
                <li>Carbon credit valuation</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <Shield className="h-12 w-12 text-blue-600 mb-4" />
              <CardTitle>Compliance Engine</CardTitle>
              <CardDescription>
                Automated checking against EBRD, IFC, and EU Taxonomy standards
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>Environmental standards verification</li>
                <li>Local content requirements</li>
                <li>ESG scoring</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Trusted By Section */}
      <section className="container mx-auto px-4 py-20">
        <h3 className="text-2xl font-semibold text-center mb-8">Trusted by Leading Institutions</h3>
        <div className="flex flex-wrap justify-center items-center gap-12 opacity-60">
          <div className="text-3xl font-bold">EBRD</div>
          <div className="text-3xl font-bold">EIB</div>
          <div className="text-3xl font-bold">AfDB</div>
          <div className="text-3xl font-bold">BII</div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Transform Your Infrastructure Finance?</h2>
          <p className="text-xl mb-8 opacity-90">Join leading institutions in accelerating energy transition projects</p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/dashboard">
              <Button size="lg" variant="secondary" className="text-lg px-8">
                Start Free Pilot
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="#demo">
              <Button size="lg" variant="outline" className="text-lg px-8 bg-transparent border-white text-white hover:bg-white/10">
                View Case Studies
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Zap className="h-6 w-6" />
                <span className="text-xl font-bold">InfraFlow AI</span>
              </div>
              <p className="text-gray-400">
                Transforming infrastructure finance with artificial intelligence
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="#features">Features</Link></li>
                <li><Link href="#solutions">Solutions</Link></li>
                <li><Link href="/dashboard">Dashboard</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="#about">About</Link></li>
                <li><Link href="#case-studies">Case Studies</Link></li>
                <li><Link href="#contact">Contact</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="#privacy">Privacy</Link></li>
                <li><Link href="#terms">Terms</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
            <p>&copy; 2024 InfraFlow AI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

function FeatureItem({ icon, text }: { icon: React.ReactNode; text: string }) {
  return (
    <div className="flex items-center space-x-3">
      <div className="text-blue-600">{icon}</div>
      <span className="text-lg">{text}</span>
    </div>
  );
}
