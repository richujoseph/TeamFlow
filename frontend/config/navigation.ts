import {
  LayoutDashboard,
  CheckSquare,
  Users,
  Building,
  Briefcase,
  Calendar,
  FileText,
  Settings,
  Bell,
  ShieldAlert,
} from "lucide-react";
import { NavSection } from "@/types";

export const DASHBOARD_NAV: NavSection[] = [
  {
    title: "Overview",
    items: [
      {
        title: "Dashboard",
        href: "/dashboard",
        icon: LayoutDashboard,
      },
      {
        title: "My Tasks",
        href: "/dashboard/tasks",
        icon: CheckSquare,
      },
      {
        title: "Notifications",
        href: "/dashboard/notifications",
        icon: Bell,
      },
    ],
  },
  {
    title: "Organization",
    items: [
      {
        title: "Projects",
        href: "/dashboard/projects",
        icon: Briefcase,
      },
      {
        title: "Teams",
        href: "/dashboard/teams",
        icon: Users,
      },
      {
        title: "Meetings",
        href: "/dashboard/meetings",
        icon: Calendar,
      },
      {
        title: "Reports",
        href: "/dashboard/reports",
        icon: FileText,
      },
      {
        title: "Company",
        href: "/dashboard/company",
        icon: Building,
      },
    ],
  },
  {
    title: "System",
    items: [
      {
        title: "Settings",
        href: "/dashboard/settings",
        icon: Settings,
      },
      {
        title: "Audit Logs",
        href: "/dashboard/audit",
        icon: ShieldAlert,
      },
    ],
  },
];
