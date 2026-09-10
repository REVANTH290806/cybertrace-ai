import React from "react";
import { useNavigate } from "react-router-dom";
import { Check, ChevronRight, ChevronLeft, X, Sparkles, AlertTriangle } from "lucide-react";
import { useApp } from "../context/AppContext";

export const DemoWizard: React.FC = () => {
  const { isDemoActive, demoStep, setDemoStep, stopDemo, setActiveCaseId, updateCaseStatus } = useApp();
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

  const goToStep = (stepNumber: number) => {
    if (stepNumber < 1 || stepNumber > 10) return;
    setDemoStep(stepNumber);
    const target = steps[stepNumber - 1];
    if (target) {
      setActiveCaseId("CYB-1024");
      navigate(target.route);
    }
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
        <button onClick={stopDemo} className="text-slate-400 hover:text-white p-1 cursor-pointer">
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
          className="w-full py-2 px-3 rounded bg-blue-600 hover:bg-blue-500 text-white font-medium text-xs flex items-center justify-center space-x-2 transition-colors mb-3 cursor-pointer shadow"
        >
          <span>{current.actionText}</span>
          <ChevronRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Navigation Footer */}
      <div className="flex items-center justify-between pt-2 border-t border-slate-800/80 text-xs">
        <button
          onClick={() => goToStep(demoStep - 1)}
          disabled={demoStep === 1}
          className="flex items-center space-x-1 text-slate-400 hover:text-white disabled:opacity-30 cursor-pointer"
        >
          <ChevronLeft className="w-3.5 h-3.5" />
          <span>Previous</span>
        </button>

        <div className="flex space-x-1">
          {steps.map((s) => (
            <button
              key={s.step}
              onClick={() => goToStep(s.step)}
              className={`w-2.5 h-2.5 rounded-full transition-all cursor-pointer ${
                s.step === demoStep ? "bg-blue-400 scale-125" : s.step < demoStep ? "bg-blue-600" : "bg-slate-700 hover:bg-slate-600"
              }`}
              title={`Jump to Step ${s.step}`}
            />
          ))}
        </div>

        {demoStep < 10 ? (
          <button
            onClick={() => goToStep(demoStep + 1)}
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
