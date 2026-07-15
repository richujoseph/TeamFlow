"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger, SheetTitle } from "@/components/ui/sheet";
import { ScrollArea } from "@/components/ui/scroll-area";
import { DASHBOARD_NAV } from "@/config/navigation";
import { Logo } from "@/components/shared/logo";
import { cn } from "@/lib/utils";
import { VisuallyHidden } from "@radix-ui/react-visually-hidden";

export function MobileNav() {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger>
        <Button variant="ghost" size="icon" className="md:hidden shrink-0">
          <Menu className="size-5" />
          <span className="sr-only">Toggle navigation menu</span>
        </Button>
      </SheetTrigger>
      <SheetContent side="left" className="w-72 p-0 flex flex-col">
        <VisuallyHidden>
            <SheetTitle>Navigation Menu</SheetTitle>
        </VisuallyHidden>
        <div className="flex h-14 items-center border-b px-4">
          <Logo />
        </div>
        <ScrollArea className="flex-1 py-4">
          <nav className="flex flex-col gap-6 px-4">
            {DASHBOARD_NAV.map((section, index) => (
              <div key={index} className="flex flex-col gap-2">
                <h4 className="px-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  {section.title}
                </h4>
                {section.items.map((item, itemIndex) => {
                  const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
                  return (
                    <Link
                      key={itemIndex}
                      href={item.href}
                      onClick={() => setOpen(false)}
                    >
                      <Button
                        variant={isActive ? "secondary" : "ghost"}
                        className={cn(
                          "h-10 w-full justify-start gap-3",
                          isActive && "bg-secondary font-medium"
                        )}
                      >
                        <item.icon className="size-5 shrink-0" />
                        <span className="truncate">{item.title}</span>
                      </Button>
                    </Link>
                  );
                })}
              </div>
            ))}
          </nav>
        </ScrollArea>
      </SheetContent>
    </Sheet>
  );
}
