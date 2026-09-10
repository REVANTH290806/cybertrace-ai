import React from "react";
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
