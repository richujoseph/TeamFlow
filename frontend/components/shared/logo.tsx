import Link from "next/link";
import { cn } from "@/lib/utils";

interface LogoProps {
  className?: string;
  collapsed?: boolean;
}

export function Logo({ className, collapsed = false }: LogoProps) {
  return (
    <Link href="/dashboard" className={cn("flex items-center gap-2", className)}>
      <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          strokeWidth="2" 
          strokeLinecap="round" 
          strokeLinejoin="round" 
          className="size-5"
        >
          <circle cx="12" cy="5" r="2" />
          <circle cx="19" cy="12" r="2" />
          <circle cx="12" cy="19" r="2" />
          <circle cx="5" cy="12" r="2" />
          <path d="M12 7v3" />
          <path d="M17 12h-3" />
          <path d="M12 17v-3" />
          <path d="M7 12h3" />
          <circle cx="12" cy="12" r="2" />
        </svg>
      </div>
      {!collapsed && (
        <span className="text-xl font-bold tracking-tight">TeamFlow</span>
      )}
    </Link>
  );
}
