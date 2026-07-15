export default function DashboardPage() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome back to TeamFlow. Here is an overview of your projects and tasks.
        </p>
      </div>
      
      {/* Skeleton for future widgets */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="rounded-xl border bg-card text-card-foreground shadow h-32 p-6 flex flex-col justify-between">
            <div className="h-4 w-1/2 rounded bg-muted animate-pulse"></div>
            <div className="h-8 w-3/4 rounded bg-muted animate-pulse"></div>
          </div>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7 mt-4">
        <div className="rounded-xl border bg-card text-card-foreground shadow lg:col-span-4 h-96 p-6">
          <div className="h-6 w-1/3 rounded bg-muted animate-pulse mb-4"></div>
          <div className="h-full w-full rounded bg-muted/50 animate-pulse"></div>
        </div>
        <div className="rounded-xl border bg-card text-card-foreground shadow lg:col-span-3 h-96 p-6">
          <div className="h-6 w-1/2 rounded bg-muted animate-pulse mb-4"></div>
          <div className="space-y-4">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="h-12 w-full rounded bg-muted/50 animate-pulse"></div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
