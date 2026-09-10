import React from "react";

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
