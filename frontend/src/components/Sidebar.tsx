import React from "react";
import { NavLink } from "react-router-dom";
import {
  ShieldAlert, LayoutDashboard, FolderSearch, Database,
  GitFork, BrainCircuit, Map, Bell, BarChart3, FileText,
  Settings, CheckCircle2
} from "lucide-react";
import { useApp } from "../context/AppContext";

export const Sidebar: React.FC = () => {
  const { unreadAlertsCount } = useApp();

  const navItems = [
    { label: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
    { label: "Cases", path: "/cases", icon: FolderSearch },
    { label: "Data Ingestion", path: "/ingestion", icon: Database },
    { label: "Transactions", path: "/transactions", icon: GitFork },
    { label: "AI Prediction", path: "/predict", icon: BrainCircuit },
    { label: "Risk Map", path: "/map", icon: Map },
    { label: "Alerts", path: "/alerts", icon: Bell, badge: unreadAlertsCount },
    { label: "Analytics", path: "/analytics", icon: BarChart3 },
    { label: "Reports", path: "/reports", icon: FileText },
    { label: "Settings", path: "/settings", icon: Settings },
  ];

  return (
    <aside className="w-64 bg-[#090e1f] border-r border-slate-800/90 flex flex-col shrink-0 select-none">
      {/* Brand */}
      <div className="p-4 border-b border-slate-800/90 flex items-center space-x-3 bg-[#0d152f]">
        <div className="p-2 bg-blue-600/20 border border-blue-500/40 rounded-lg text-blue-400">
          <ShieldAlert className="w-6 h-6" />
        </div>
        <div>
          <h1 className="text-base font-bold text-white tracking-wider">CYBERTRACE AI</h1>
          <p className="text-[10px] text-slate-400 uppercase tracking-wider">Cash Withdrawal Intel</p>
        </div>
      </div>

      {/* Nav items */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto custom-scrollbar">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center justify-between px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-blue-600/25 text-blue-400 border border-blue-500/40"
                    : "text-slate-300 hover:bg-slate-800/60 hover:text-white"
                }`
              }
            >
              <div className="flex items-center space-x-3">
                <Icon className="w-4 h-4 text-slate-400" />
                <span>{item.label}</span>
              </div>
              {item.badge !== undefined && item.badge > 0 && (
                <span className="px-2 py-0.5 text-xs font-bold bg-red-600 text-white rounded-full">
                  {item.badge}
                </span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Footer System Status */}
      <div className="p-3 border-t border-slate-800/90 bg-[#060a17] text-xs space-y-1.5">
        <div className="flex items-center justify-between text-slate-400">
          <span className="flex items-center space-x-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="font-mono text-[11px] text-slate-300">System Online</span>
          </span>
          <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-blue-950 text-blue-400 border border-blue-800/50">
            PROTOTYPE
          </span>
        </div>
        <p className="text-[10px] text-slate-500 font-mono truncate">
          SIH26184 // CID Karnataka
        </p>
      </div>
    </aside>
  );
};
