import os

src_dir = "/Users/revanth/.gemini/antigravity/scratch/cybertrace-ai/frontend/src/components"

# 1. StatusBadge.tsx
with open(os.path.join(src_dir, "StatusBadge.tsx"), "w") as f:
    f.write('''import React from "react";

interface StatusBadgeProps {
  type: "risk" | "status";
  value: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ type, value }) => {
  if (type === "risk") {
    const val = value.toUpperCase();
    if (val === "HIGH") {
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-semibold bg-red-950/80 text-red-400 border border-red-800/80">
          HIGH RISK
        </span>
      );
    }
    if (val === "MEDIUM") {
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-semibold bg-amber-950/80 text-amber-400 border border-amber-800/80">
          MEDIUM RISK
        </span>
      );
    }
    return (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-semibold bg-emerald-950/80 text-emerald-400 border border-emerald-800/80">
        LOW RISK
      </span>
    );
  }

  // Status type
  const statusStyles: Record<string, string> = {
    NEW: "bg-blue-950/80 text-blue-400 border-blue-800",
    "UNDER ANALYSIS": "bg-indigo-950/80 text-indigo-400 border-indigo-800",
    "HIGH-RISK PREDICTION": "bg-rose-950/80 text-rose-400 border-rose-800",
    "ALERT GENERATED": "bg-red-950/80 text-red-400 border-red-800",
    "ACTION INITIATED": "bg-orange-950/80 text-orange-400 border-orange-800",
    MONITORING: "bg-amber-950/80 text-amber-400 border-amber-800",
    RESOLVED: "bg-emerald-950/80 text-emerald-400 border-emerald-800"
  };

  const style = statusStyles[value] || "bg-slate-800 text-slate-300 border-slate-700";

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium border ${style}`}>
      {value}
    </span>
  );
};
''')

# 2. Sidebar.tsx
with open(os.path.join(src_dir, "Sidebar.tsx"), "w") as f:
    f.write('''import React from "react";
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
''')

# 3. Header.tsx
with open(os.path.join(src_dir, "Header.tsx"), "w") as f:
    f.write('''import React from "react";
import { Play, AlertCircle, Shield, ChevronDown } from "lucide-react";
import { useApp } from "../context/AppContext";

export const Header: React.FC = () => {
  const { cases, activeCaseId, setActiveCaseId, startDemo, user } = useApp();

  return (
    <header className="bg-[#0c1328] border-b border-slate-800 px-6 py-2.5 flex flex-col space-y-2 select-none shrink-0">
      {/* Disclaimer Banner */}
      <div className="bg-amber-950/60 border border-amber-800/50 px-3 py-1 rounded text-xs text-amber-300 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <AlertCircle className="w-3.5 h-3.5 shrink-0 text-amber-400" />
          <span className="font-medium text-[11px]">
            Prototype demonstration using synthetic/anonymized data. Predictions are decision-support outputs and are not definitive law-enforcement conclusions.
          </span>
        </div>
        <span className="text-[10px] font-mono uppercase text-amber-400/80 ml-2">SIH-2024 / SIH26184</span>
      </div>

      {/* Main Bar */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active Case:</span>
            <div className="relative">
              <select
                value={activeCaseId}
                onChange={(e) => setActiveCaseId(e.target.value)}
                className="bg-slate-900 border border-slate-700 text-white text-xs font-mono rounded px-3 py-1.5 pr-8 focus:outline-none focus:border-blue-500 cursor-pointer appearance-none"
              >
                {cases.map((c) => (
                  <option key={c.case_id} value={c.case_id}>
                    {c.case_id} — {c.fraud_type} ({c.risk_level})
                  </option>
                ))}
              </select>
              <ChevronDown className="w-3.5 h-3.5 text-slate-400 absolute right-2.5 top-2.5 pointer-events-none" />
            </div>
          </div>

          {activeCaseId === "CYB-1024" && (
            <span className="px-2 py-0.5 text-[11px] font-semibold bg-blue-900/60 text-blue-300 border border-blue-700 rounded">
              SIH Showcase Case
            </span>
          )}
        </div>

        <div className="flex items-center space-x-4">
          {/* Prominent Demo Mode Button */}
          <button
            onClick={startDemo}
            className="flex items-center space-x-2 px-3.5 py-1.5 rounded bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold text-xs shadow-md border border-blue-400/30 transition-all cursor-pointer"
          >
            <Play className="w-3.5 h-3.5 fill-current text-white" />
            <span>START DEMO</span>
          </button>

          {/* Officer Info */}
          <div className="flex items-center space-x-2.5 pl-3 border-l border-slate-700">
            <div className="w-7 h-7 rounded bg-slate-800 border border-slate-700 flex items-center justify-center text-blue-400">
              <Shield className="w-4 h-4" />
            </div>
            <div className="text-left">
              <div className="text-xs font-semibold text-slate-200">{user?.full_name || "Demo Officer"}</div>
              <div className="text-[10px] text-slate-400 font-mono">{user?.badge_number || "CYB-BLR-089"}</div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};
''')

# 4. DemoWizard.tsx
with open(os.path.join(src_dir, "DemoWizard.tsx"), "w") as f:
    f.write('''import React from "react";
import { useNavigate } from "react-router-dom";
import { Check, ChevronRight, ChevronLeft, X, Sparkles, AlertTriangle } from "lucide-react";
import { useApp } from "../context/AppContext";

export const DemoWizard: React.FC = () => {
  const { isDemoActive, demoStep, nextDemoStep, prevDemoStep, stopDemo, setActiveCaseId, updateCaseStatus } = useApp();
  const navigate = useNavigate();

  if (!isDemoActive) return null;

  const steps = [
    {
      step: 1,
      title: "Step 1: Cybercrime Complaint Received",
      desc: "Victim Rajesh Kumar files complaint NCRP-2026-8921 regarding ₹1,85,000 lost in UPI impersonation fraud.",
      route: "/cases",
      actionText: "Inspect Complaint Details"
    },
    {
      step: 2,
      title: "Step 2: Transaction Data Ingested",
      desc: "Bank transaction feeds automatically ingested and synchronized through Section 91 CrPC compliance gateway.",
      route: "/ingestion",
      actionText: "View Ingestion Pipeline"
    },
    {
      step: 3,
      title: "Step 3: Suspicious Mule Account Detected",
      desc: "Algorithmic screening flags dormant account ACC-MULE-204 reactivated with zero historical KYC activity.",
      route: "/transactions",
      actionText: "Inspect Mule Account Node"
    },
    {
      step: 4,
      title: "Step 4: Transaction Network Mapped",
      desc: "Interactive graph visualizes 4-hop fund layering from Victim → Layer 1 → Layer 2 → Layer 3 → Mule Account.",
      route: "/transactions",
      actionText: "Trace Money Trail Graph"
    },
    {
      step: 5,
      title: "Step 5: AI Risk Analysis Executed",
      desc: "Random Forest engine calculates 87.4% withdrawal probability based on transaction velocity (82%) and time pattern.",
      route: "/predict",
      actionText: "Analyze Model Factors"
    },
    {
      step: 6,
      title: "Step 6: Likely Withdrawal Location Predicted",
      desc: "Engine forecasts imminent liquidation at ATM A102 (Koramangala 80ft Rd) in window 23:30 – 00:30.",
      route: "/predict",
      actionText: "View Forecast Window"
    },
    {
      step: 7,
      title: "Step 7: Risk Appears on Bengaluru Map",
      desc: "Target kiosk ATM A102 highlighted in RED on high-risk geographic heatmap in Koramangala police jurisdiction.",
      route: "/map",
      actionText: "Locate ATM on Leaflet Map"
    },
    {
      step: 8,
      title: "Step 8: High-Risk Alert Generated",
      desc: "Priority alert ALT-1024 automatically dispatched to Central Cyber Command console and field dispatch units.",
      route: "/alerts",
      actionText: "Review Real-Time Alert"
    },
    {
      step: 9,
      title: "Step 9: Officer Action Initiated",
      desc: "Investigating Officer issues Section 102 debit freeze to SBI and dispatches Koramangala Sector 4 Patrol.",
      route: "/cases",
      actionText: "Trigger Field Dispatch",
      action: async () => {
        await updateCaseStatus("ACTION INITIATED", "Field team dispatched to Koramangala ATM A102 perimeter.");
      }
    },
    {
      step: 10,
      title: "Step 10: Case Moved to Monitoring & Report Generated",
      desc: "ATM surveillance active; formal court-admissible Cyber Intelligence Dossier compiled with timestamped evidence.",
      route: "/reports",
      actionText: "Generate Investigation Report",
      action: async () => {
        await updateCaseStatus("MONITORING", "Target ATM placed under active physical and CCTV monitoring.");
      }
    }
  ];

  const current = steps[demoStep - 1] || steps[0];

  const handleStepAction = async () => {
    setActiveCaseId("CYB-1024");
    if (current.action) {
      await current.action();
    }
    navigate(current.route);
  };

  return (
    <div className="fixed bottom-5 right-6 z-50 w-[440px] bg-[#0c142c] border-2 border-blue-500/80 rounded-xl shadow-2xl p-4 text-slate-100 backdrop-blur-md">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <div className="p-1.5 bg-blue-500/20 text-blue-400 rounded-md">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-blue-400">SIH Judge Demonstration</h3>
            <p className="text-[11px] text-slate-400">Step {demoStep} of 10: Showcase Case CYB-1024</p>
          </div>
        </div>
        <button onClick={stopDemo} className="text-slate-400 hover:text-white p-1">
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Progress bar */}
      <div className="w-full bg-slate-800 h-1.5 rounded-full my-3 overflow-hidden">
        <div
          className="bg-gradient-to-r from-blue-500 to-indigo-500 h-full transition-all duration-300"
          style={{ width: `${(demoStep / 10) * 100}%` }}
        />
      </div>

      {/* Content */}
      <div className="py-1">
        <h4 className="text-sm font-bold text-white mb-1">{current.title}</h4>
        <p className="text-xs text-slate-300 leading-relaxed mb-3">{current.desc}</p>

        <button
          onClick={handleStepAction}
          className="w-full py-2 px-3 rounded bg-blue-600 hover:bg-blue-500 text-white font-medium text-xs flex items-center justify-center space-x-2 transition-colors mb-3 cursor-pointer"
        >
          <span>{current.actionText}</span>
          <ChevronRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Navigation Footer */}
      <div className="flex items-center justify-between pt-2 border-t border-slate-800/80 text-xs">
        <button
          onClick={prevDemoStep}
          disabled={demoStep === 1}
          className="flex items-center space-x-1 text-slate-400 hover:text-white disabled:opacity-30 cursor-pointer"
        >
          <ChevronLeft className="w-3.5 h-3.5" />
          <span>Previous</span>
        </button>

        <div className="flex space-x-1">
          {steps.map((s) => (
            <span
              key={s.step}
              className={`w-2 h-2 rounded-full transition-all ${
                s.step === demoStep ? "bg-blue-400 scale-125" : s.step < demoStep ? "bg-blue-600" : "bg-slate-700"
              }`}
            />
          ))}
        </div>

        {demoStep < 10 ? (
          <button
            onClick={() => {
              nextDemoStep();
              const next = steps[demoStep];
              if (next) navigate(next.route);
            }}
            className="flex items-center space-x-1 text-blue-400 hover:text-blue-300 font-semibold cursor-pointer"
          >
            <span>Next Step</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        ) : (
          <button
            onClick={stopDemo}
            className="flex items-center space-x-1 text-emerald-400 hover:text-emerald-300 font-semibold cursor-pointer"
          >
            <Check className="w-3.5 h-3.5" />
            <span>Finish Demo</span>
          </button>
        )}
      </div>
    </div>
  );
};
''')

# 5. TransactionGraph.tsx
with open(os.path.join(src_dir, "TransactionGraph.tsx"), "w") as f:
    f.write('''import React, { useState } from "react";
import { Shield, ArrowRight, UserCheck, AlertTriangle, Landmark, MapPin } from "lucide-react";
import { TransactionGraphData, GraphNode } from "../types";

interface TransactionGraphProps {
  data: TransactionGraphData;
  onSelectNode?: (node: GraphNode) => void;
}

export const TransactionGraph: React.FC<TransactionGraphProps> = ({ data, onSelectNode }) => {
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(data.nodes[0] || null);

  const handleNodeClick = (node: GraphNode) => {
    setSelectedNode(node);
    if (onSelectNode) onSelectNode(node);
  };

  const getNodeColor = (type: string) => {
    switch (type) {
      case "VICTIM":
        return { bg: "bg-blue-950/90", border: "border-blue-500", text: "text-blue-400", badge: "VICTIM" };
      case "INTERMEDIARY":
      case "SUSPICIOUS":
        return { bg: "bg-amber-950/90", border: "border-amber-500", text: "text-amber-400", badge: "LAYER" };
      case "MULE":
        return { bg: "bg-red-950/90", border: "border-red-500", text: "text-red-400", badge: "MULE ACCOUNT" };
      case "ATM":
        return { bg: "bg-rose-950/90", border: "border-rose-400", text: "text-rose-300", badge: "TARGET ATM" };
      default:
        return { bg: "bg-slate-900", border: "border-slate-600", text: "text-slate-300", badge: "NODE" };
    }
  };

  return (
    <div className="flex flex-col h-full bg-[#0b1226] border border-slate-800 rounded-lg p-4">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <h3 className="text-sm font-bold text-white">Interactive Money Trail Network</h3>
          <p className="text-xs text-slate-400">Fund dissipation sequence from source victim to forecast cash-out point</p>
        </div>
        <div className="flex items-center space-x-3 text-xs">
          <span className="flex items-center space-x-1.5"><span className="w-2.5 h-2.5 rounded-full bg-blue-500"></span><span className="text-slate-300">Victim</span></span>
          <span className="flex items-center space-x-1.5"><span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span><span className="text-slate-300">Layering Hops</span></span>
          <span className="flex items-center space-x-1.5"><span className="w-2.5 h-2.5 rounded-full bg-red-500"></span><span className="text-slate-300">Mule Node</span></span>
          <span className="flex items-center space-x-1.5"><span className="w-2.5 h-2.5 rounded-full bg-rose-400"></span><span className="text-slate-300">Target ATM</span></span>
        </div>
      </div>

      {/* Flow Sequence Cards */}
      <div className="py-6 overflow-x-auto custom-scrollbar flex items-center space-x-3 min-h-[160px]">
        {data.nodes.map((node, idx) => {
          const style = getNodeColor(node.type);
          const isSelected = selectedNode?.id === node.id;
          const edge = data.edges[idx];

          return (
            <React.Fragment key={node.id}>
              {/* Node Card */}
              <div
                onClick={() => handleNodeClick(node)}
                className={`w-52 shrink-0 p-3.5 rounded-lg border-2 cursor-pointer transition-all ${style.bg} ${
                  isSelected ? `${style.border} ring-2 ring-blue-400/50 scale-105 shadow-xl` : "border-slate-800 hover:border-slate-600"
                }`}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded ${style.bg} ${style.text} border ${style.border}`}>
                    {style.badge}
                  </span>
                  <span className="text-[11px] font-mono text-slate-400">
                    Risk: <span className={node.risk_score > 75 ? "text-red-400 font-bold" : "text-amber-400 font-bold"}>{node.risk_score}%</span>
                  </span>
                </div>
                <div className="text-xs font-bold text-white truncate">{node.label}</div>
                <div className="text-[11px] font-mono text-slate-400 truncate mt-0.5">{node.id}</div>
                <div className="text-[10px] text-slate-400 mt-2 flex items-center justify-between pt-1 border-t border-slate-800/80">
                  <span className="truncate">{node.bank}</span>
                  <span className="font-mono text-slate-500">{node.kyc}</span>
                </div>
              </div>

              {/* Edge arrow with amount and channel */}
              {edge && idx < data.nodes.length - 1 && (
                <div className="flex flex-col items-center justify-center shrink-0 px-1">
                  <span className={`text-[10px] font-bold font-mono px-2 py-0.5 rounded ${edge.is_predicted ? "bg-rose-950 text-rose-300 border border-rose-800" : "bg-slate-900 text-slate-200 border border-slate-700"}`}>
                    ₹{edge.amount.toLocaleString()}
                  </span>
                  <div className="flex items-center text-slate-500 my-1">
                    <div className={`w-8 h-[2px] ${edge.is_predicted ? "bg-rose-500 border-dashed" : "bg-blue-500"}`} />
                    <ArrowRight className={`w-4 h-4 -ml-1 ${edge.is_predicted ? "text-rose-400 animate-pulse" : "text-blue-400"}`} />
                  </div>
                  <span className="text-[9px] font-mono text-slate-400">
                    {edge.channel} ({edge.timestamp})
                  </span>
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* Selected Node Details Drawer */}
      {selectedNode && (
        <div className="mt-auto bg-slate-900/90 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <span className="text-xs font-bold text-white">{selectedNode.label}</span>
              <span className="text-xs font-mono text-slate-400">({selectedNode.id})</span>
              <span className={`text-[10px] px-2 py-0.5 rounded font-semibold ${getNodeColor(selectedNode.type).text} bg-slate-800 border border-slate-700`}>
                {selectedNode.type}
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Institution: <span className="text-slate-200 font-medium">{selectedNode.bank}</span> &bull; KYC Status: <span className="text-slate-200 font-medium">{selectedNode.kyc}</span>
            </p>
          </div>

          <div className="flex items-center space-x-6 text-xs font-mono">
            <div>
              <span className="text-slate-500 block text-[10px]">RISK CLASSIFICATION</span>
              <span className={`font-bold ${selectedNode.risk_score > 70 ? "text-red-400" : "text-amber-400"}`}>
                {selectedNode.risk_score}% ({selectedNode.risk_score > 70 ? "HIGH RISK" : "MODERATE"})
              </span>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px]">INTELLIGENCE DIRECTIVE</span>
              <span className="text-slate-300">
                {selectedNode.type === "MULE" ? "Issue Sec 102 CrPC Freeze" : selectedNode.type === "ATM" ? "Deploy Perimeter Patrol" : "Subpoena Statement"}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
''')

print("StatusBadge, Sidebar, Header, DemoWizard, TransactionGraph written successfully.")
