"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { useSidebar } from "@/hooks/use-sidebar";
import { DASHBOARD_NAV } from "@/config/navigation";
import { Logo } from "@/components/shared/logo";
import { ChevronLeft, ChevronRight } from "lucide-react";

export function Sidebar() {
  const pathname = usePathname();
  const { isOpen, toggle } = useSidebar();

  return (
    <aside
      className={cn(
        "relative hidden h-screen flex-col border-r bg-background transition-all duration-300 ease-in-out md:flex",
        isOpen ? "w-64" : "w-[72px]"
      )}
    >
      <div className="flex h-14 items-center border-b px-4 py-4">
        <Logo collapsed={!isOpen} className={!isOpen ? "mx-auto" : ""} />
      </div>

      <ScrollArea className="flex-1 px-3 py-4">
        <nav className="flex flex-col gap-6">
          {DASHBOARD_NAV.map((section, index) => (
            <div key={index} className="flex flex-col gap-2">
              {isOpen && (
                <h4 className="px-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  {section.title}
                </h4>
              )}
              {section.items.map((item, itemIndex) => {
                const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
                
                if (!isOpen) {
                  return (
                    <Tooltip key={itemIndex} delayDuration={0}>
                      <TooltipTrigger asChild>
                        <Link href={item.href}>
                          <Button
                            variant={isActive ? "secondary" : "ghost"}
                            className={cn("h-10 w-full justify-center px-0", isActive && "bg-secondary")}
                          >
                            <item.icon className="size-5" />
                            <span className="sr-only">{item.title}</span>
                          </Button>
                        </Link>
                      </TooltipTrigger>
                      <TooltipContent side="right" className="font-semibold">
                        {item.title}
                      </TooltipContent>
                    </Tooltip>
                  );
                }

                return (
                  <Link key={itemIndex} href={item.href}>
                    <Button
                      variant={isActive ? "secondary" : "ghost"}
                      className={cn(
                        "h-10 w-full justify-start gap-3 px-3",
                        isActive && "bg-secondary font-medium"
                      )}
                    >
                      <item.icon className="size-5 shrink-0" />
                      <span className="truncate">{item.title}</span>
                      {item.label && (
                        <span className="ml-auto rounded-full bg-primary/10 px-2 py-0.5 text-xs font-medium text-primary">
                          {item.label}
                        </span>
                      )}
                    </Button>
                  </Link>
                );
              })}
            </div>
          ))}
        </nav>
      </ScrollArea>

      <div className="border-t p-3">
        <Button
          variant="ghost"
          size="icon"
          className="ml-auto flex size-8 items-center justify-center rounded-full"
          onClick={toggle}
        >
          {isOpen ? <ChevronLeft className="size-4" /> : <ChevronRight className="size-4" />}
          <span className="sr-only">Toggle Sidebar</span>
        </Button>
      </div>
    </aside>
  );
}
