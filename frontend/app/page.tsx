"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, CheckCircle2, Workflow, Activity, Users, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";

const features = [
  {
    name: "Agile Project Management",
    description: "Plan, track, and manage agile and software projects from a single platform.",
    icon: Workflow,
  },
  {
    name: "Real-time Collaboration",
    description: "Keep your engineering team aligned with real-time updates and discussions.",
    icon: Users,
  },
  {
    name: "Advanced Analytics",
    description: "Generate deep engineering reports and metrics with a single click.",
    icon: Activity,
  },
  {
    name: "Automated Documentation",
    description: "Automatically compile release notes, meeting minutes, and architectural decisions.",
    icon: FileText,
  },
];

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-zinc-50 dark:bg-zinc-950 overflow-hidden">
      {/* Background decorations */}
      <div className="absolute top-0 -translate-y-12 left-1/2 -translate-x-1/2 w-[800px] h-[500px] opacity-20 dark:opacity-30 pointer-events-none">
        <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 blur-[100px] rounded-full mix-blend-multiply dark:mix-blend-screen" />
      </div>

      <header className="sticky top-0 z-50 w-full border-b border-zinc-200 dark:border-zinc-800 bg-white/80 dark:bg-zinc-950/80 backdrop-blur-md">
        <div className="container mx-auto flex h-16 items-center justify-between px-4 sm:px-8">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600 text-white shadow-lg">
              <Workflow size={20} />
            </div>
            <span className="text-xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">TeamFlow</span>
          </div>
          <div className="flex items-center gap-4">
            <Button variant="ghost" asChild className="hidden sm:flex">
              <Link href="/login">Log in</Link>
            </Button>
            <Button asChild className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-md">
              <Link href="/register">Get Started</Link>
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative px-4 pt-24 pb-32 sm:px-6 lg:px-8 flex flex-col items-center text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="z-10 max-w-4xl"
          >
            <div className="inline-flex items-center rounded-full border border-zinc-200 dark:border-zinc-800 bg-white/50 dark:bg-zinc-900/50 px-3 py-1 text-sm font-medium text-zinc-600 dark:text-zinc-300 backdrop-blur-sm mb-8 shadow-sm">
              <span className="flex h-2 w-2 rounded-full bg-indigo-500 mr-2 animate-pulse" />
              TeamFlow v1.0 is now in preview
            </div>
            <h1 className="text-5xl sm:text-6xl md:text-7xl font-extrabold tracking-tight text-zinc-900 dark:text-white mb-6">
              Engineering management, <br className="hidden sm:block" />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 to-purple-600">
                beautifully unified.
              </span>
            </h1>
            <p className="mt-6 text-lg sm:text-xl leading-8 text-zinc-600 dark:text-zinc-400 max-w-2xl mx-auto">
              The all-in-one enterprise platform that brings Jira, GitLab Issues, and Confluence into one seamless experience.
              Built specifically for modern software engineering teams.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Button asChild size="lg" className="h-12 px-8 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full shadow-lg shadow-indigo-500/20 transition-all hover:scale-105">
                <Link href="/dashboard">
                  Go to Dashboard <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg" className="h-12 px-8 rounded-full border-zinc-300 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-all">
                <Link href="/docs">Read the Docs</Link>
              </Button>
            </div>
          </motion.div>

          {/* Dashboard Preview Mockup */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.2 }}
            className="mt-20 relative w-full max-w-5xl mx-auto"
          >
            <div className="rounded-xl border border-zinc-200/50 dark:border-zinc-800/50 bg-white/40 dark:bg-zinc-950/40 p-2 backdrop-blur-xl shadow-2xl">
              <div className="rounded-lg overflow-hidden border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 aspect-video relative flex items-center justify-center">
                <div className="absolute inset-0 bg-zinc-50 dark:bg-zinc-900/50 flex flex-col">
                  {/* Mock UI Header */}
                  <div className="h-12 border-b border-zinc-200 dark:border-zinc-800 flex items-center px-4 gap-4">
                    <div className="flex gap-1.5">
                      <div className="w-3 h-3 rounded-full bg-red-400" />
                      <div className="w-3 h-3 rounded-full bg-amber-400" />
                      <div className="w-3 h-3 rounded-full bg-green-400" />
                    </div>
                    <div className="h-6 w-64 bg-zinc-200 dark:bg-zinc-800 rounded-md ml-4" />
                  </div>
                  {/* Mock UI Body */}
                  <div className="flex-1 flex p-4 gap-4">
                    <div className="w-48 hidden sm:flex flex-col gap-2">
                      {[1, 2, 3, 4, 5].map((i) => (
                        <div key={i} className={`h-8 rounded-md ${i === 1 ? 'bg-indigo-100 dark:bg-indigo-900/30' : 'bg-zinc-100 dark:bg-zinc-800/50'}`} />
                      ))}
                    </div>
                    <div className="flex-1 flex flex-col gap-4">
                      <div className="flex justify-between items-center">
                        <div className="h-8 w-48 bg-zinc-200 dark:bg-zinc-800 rounded-md" />
                        <div className="h-8 w-24 bg-indigo-500 rounded-md" />
                      </div>
                      <div className="flex gap-4">
                        {[1, 2, 3].map((col) => (
                          <div key={col} className="flex-1 bg-zinc-100 dark:bg-zinc-800/30 rounded-lg p-3 flex flex-col gap-3">
                            <div className="h-5 w-24 bg-zinc-200 dark:bg-zinc-700 rounded mb-2" />
                            {[1, 2].map((card) => (
                              <div key={card} className="h-24 bg-white dark:bg-zinc-900 rounded border border-zinc-200 dark:border-zinc-700 shadow-sm" />
                            ))}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </section>

        {/* Features Section */}
        <section className="py-24 bg-white dark:bg-zinc-900 border-t border-zinc-200 dark:border-zinc-800">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold tracking-tight text-zinc-900 dark:text-white sm:text-4xl">
                Everything you need to ship faster
              </h2>
              <p className="mt-4 text-lg text-zinc-600 dark:text-zinc-400">
                Powerful features designed specifically for modern engineering teams.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, index) => (
                <motion.div 
                  key={feature.name}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  className="bg-zinc-50 dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 p-6 rounded-2xl hover:shadow-lg transition-shadow"
                >
                  <div className="h-12 w-12 rounded-lg bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center text-indigo-600 dark:text-indigo-400 mb-6">
                    <feature.icon size={24} />
                  </div>
                  <h3 className="text-xl font-semibold text-zinc-900 dark:text-white mb-3">{feature.name}</h3>
                  <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed">{feature.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      </main>

      <footer className="bg-zinc-50 dark:bg-zinc-950 border-t border-zinc-200 dark:border-zinc-800 py-12 mt-auto">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <Workflow size={20} className="text-indigo-600" />
            <span className="text-lg font-semibold text-zinc-900 dark:text-white">TeamFlow</span>
          </div>
          <p className="text-sm text-zinc-500 dark:text-zinc-400">
            &copy; {new Date().getFullYear()} TeamFlow EPMS. Built for engineering teams.
          </p>
        </div>
      </footer>
    </div>
  );
}
