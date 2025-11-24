import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-white dark:from-gray-900 dark:to-gray-800">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-6xl mb-6">
            InfraFlow AI
          </h1>
          <h2 className="text-3xl font-semibold text-blue-600 dark:text-blue-400 mb-8">
            Accelerate Energy Transition Financing with AI
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-12">
            The intelligent platform connecting $130 trillion in climate finance
            with bankable infrastructure projects.
          </p>
          <div className="flex gap-4 justify-center">
            <Button size="lg" asChild>
              <Link href="/dashboard">Start Free Pilot</Link>
            </Button>
            <Button size="lg" variant="outline" asChild>
              <Link href="/demo">Book Demo</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="grid md:grid-cols-2 gap-12 max-w-6xl mx-auto">
          {/* For DFIs */}
          <div>
            <h3 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">
              For Development Finance Institutions
            </h3>
            <ul className="space-y-4">
              {[
                '50% faster due diligence',
                'Automated compliance checking',
                'Risk prediction powered by 1000+ projects',
                'One-click investment memos',
              ].map((benefit) => (
                <li key={benefit} className="flex items-start">
                  <svg
                    className="h-6 w-6 text-green-500 mr-2 flex-shrink-0"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span className="text-lg text-gray-700 dark:text-gray-300">{benefit}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* For Project Sponsors */}
          <div>
            <h3 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">
              For Project Sponsors
            </h3>
            <ul className="space-y-4">
              {[
                'DFI-ready documentation',
                'Financial model optimization',
                'Multi-stakeholder coordination',
                'Regulatory navigation',
              ].map((benefit) => (
                <li key={benefit} className="flex items-start">
                  <svg
                    className="h-6 w-6 text-green-500 mr-2 flex-shrink-0"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span className="text-lg text-gray-700 dark:text-gray-300">{benefit}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-16 bg-white dark:bg-gray-900">
        <h3 className="text-3xl font-bold text-center mb-12 text-gray-900 dark:text-white">
          Platform Features
        </h3>
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle>Document Intelligence</CardTitle>
              <CardDescription>
                Multi-language ingestion and automated analysis
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="list-disc list-inside space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li>Extract key terms from 1000+ page documents</li>
                <li>Auto-generate executive summaries</li>
                <li>Risk factor identification</li>
                <li>Regulatory compliance checking</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Financial Modeling</CardTitle>
              <CardDescription>
                Advanced scenario analysis and risk modeling
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="list-disc list-inside space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li>DCF analysis with 10,000 scenarios</li>
                <li>Blended finance structuring</li>
                <li>Currency risk modeling</li>
                <li>Political risk quantification</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Compliance Engine</CardTitle>
              <CardDescription>
                Automated standards verification
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="list-disc list-inside space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li>EBRD Environmental Standards</li>
                <li>IFC Performance Standards</li>
                <li>EU Taxonomy alignment</li>
                <li>ESG scoring</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Trusted By Section */}
      <section className="container mx-auto px-4 py-16">
        <h3 className="text-2xl font-bold text-center mb-8 text-gray-900 dark:text-white">
          Trusted by Leading Institutions
        </h3>
        <div className="flex justify-center items-center gap-12 flex-wrap">
          <div className="text-gray-500 dark:text-gray-400 font-semibold text-lg">EBRD</div>
          <div className="text-gray-500 dark:text-gray-400 font-semibold text-lg">EIB</div>
          <div className="text-gray-500 dark:text-gray-400 font-semibold text-lg">AfDB</div>
          <div className="text-gray-500 dark:text-gray-400 font-semibold text-lg">BII</div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 mt-16">
        <div className="container mx-auto px-4 text-center">
          <p className="text-gray-400">
            &copy; 2024 InfraFlow AI. All rights reserved.
          </p>
        </div>
      </footer>
    </main>
  )
}
