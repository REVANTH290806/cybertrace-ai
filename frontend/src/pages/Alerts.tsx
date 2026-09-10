import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Bell, BellRing, AlertOctagon, CheckCircle2, Send, Radio,
  Sparkles, Filter, ShieldCheck, MapPin, IndianRupee, Eye
} from "lucide-react";
import { useApp } from "../context/AppContext";
import { api } from "../services/api";
import { AlertItem } from "../types";

export const Alerts: React.FC = () => {
  const { alerts, refreshAlerts, setActiveCaseId, simulateIncomingAlert, cases } = useApp();
  const [filter, setFilter] = useState<string>("ALL");
  const [simulating, setSimulating] = useState(false);
  const [toast, setToast] = useState<string | null>(null);
  const navigate = useNavigate();

  const showToast = (msg: string) => {
    setToast(msg);
    setTimeout(() => setToast(null), 3500);
  };

  const handleStatusUpdate = async (alertId: string, newStatus: string, actionNote: string) => {
    try {
      await api.updateAlertStatus(alertId, newStatus);
      await refreshAlerts();
      showToast(`Alert ${alertId} updated to ${newStatus}: ${actionNote}`);
    } catch (e) {
      console.error(e);
      showToast(`Error updating alert ${alertId}`);
    }
  };

  const handleSimulate = async () => {
    setSimulating(true);
    const newAlert = await simulateIncomingAlert();
    setSimulating(false);
    if (newAlert) {
      showToast(`High-risk real-time alert ${newAlert.alert_id} generated for ${newAlert.location_name || newAlert.location_id}!`);
    }
  };

  const filteredAlerts = alerts.filter((a) => {
    if (filter === "ALL") return true;
    return a.status === filter;
  });

  return (
    <div className="p-6 space-y-6">
      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-xl font-black text-white flex items-center space-x-2">
            <BellRing className="w-5 h-5 text-red-400" />
            <span>Real-Time Predictive Intercept Alert Console</span>
          </h1>
          <p className="text-xs text-slate-400">
            Automated threshold notifications (Probability &gt; 70%) for immediate tactical intervention
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleSimulate}
            disabled={simulating}
            className="px-4 py-2 rounded bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white text-xs font-bold shadow-lg flex items-center space-x-1.5 transition-all cursor-pointer"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>{simulating ? "Simulating Incoming..." : "Simulate Incoming Alert"}</span>
          </button>
        </div>
      </div>

      {toast && (
        <div className="p-3 bg-blue-950/90 border border-blue-500 text-blue-200 rounded text-xs font-semibold flex items-center justify-between shadow-lg">
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>{toast}</span>
          </div>
          <button onClick={() => setToast(null)} className="text-slate-400 hover:text-white cursor-pointer">&times;</button>
        </div>
      )}

      {/* Filter Tabs */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-2 text-xs">
        {["ALL", "ACTIVE", "ACKNOWLEDGED", "DISPATCHED", "BANK_ALERTED", "RESOLVED"].map((tab) => (
          <button
            key={tab}
            onClick={() => setFilter(tab)}
            className={`px-3 py-1.5 rounded font-semibold transition-colors cursor-pointer ${
              filter === tab
                ? "bg-blue-600 text-white shadow"
                : "bg-slate-900 text-slate-400 hover:text-white hover:bg-slate-800"
            }`}
          >
            {tab} {tab === "ACTIVE" && `(${alerts.filter(a => a.status === "ACTIVE").length})`}
          </button>
        ))}
      </div>

      {/* Alerts Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredAlerts.map((a) => (
          <div
            key={a.alert_id}
            className={`p-5 rounded-lg border-2 bg-[#0e162f] flex flex-col justify-between space-y-3 transition-all ${
              a.status === "ACTIVE" ? "border-red-600/70 shadow-lg shadow-red-950/40" : "border-slate-800"
            }`}
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-red-950 text-red-400 border border-red-800">
                    {a.severity} RISK
                  </span>
                  <span className="font-mono text-xs font-bold text-white">{a.alert_id}</span>
                </div>
                <span className="text-[10px] font-mono text-slate-500">
                  {new Date(a.created_at).toLocaleTimeString()}
                </span>
              </div>

              <div className="text-sm font-bold text-white">
                Case: <span className="text-blue-400">{a.case_id}</span> &bull; {a.location_name || a.location_id}
              </div>

              <div className="grid grid-cols-3 gap-2 my-2.5 p-2.5 bg-slate-900/80 rounded border border-slate-800 text-xs font-mono">
                <div>
                  <span className="text-slate-500 text-[10px] block">PROBABILITY</span>
                  <span className="text-red-400 font-bold">{a.probability}%</span>
                </div>
                <div>
                  <span className="text-slate-500 text-[10px] block">TIME WINDOW</span>
                  <span className="text-amber-300 font-bold">{a.expected_time}</span>
                </div>
                <div>
                  <span className="text-slate-500 text-[10px] block">AT RISK</span>
                  <span className="text-white font-bold">₹{a.amount.toLocaleString()}</span>
                </div>
              </div>

              <div className="text-xs text-slate-300 bg-slate-900/50 p-2.5 rounded border border-slate-800">
                <span className="text-[10px] font-semibold text-slate-500 uppercase block mb-0.5">Recommended Protocol</span>
                {a.recommended_action}
              </div>
            </div>

            {/* ALL 5 BUTTONS REQUIRED BY SECTION 15 */}
            <div className="pt-3 border-t border-slate-800 space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="text-[10px] text-slate-500 font-mono">Current Status:</span>
                <span className="text-[10px] font-bold font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-200 border border-slate-700">
                  {a.status}
                </span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-5 gap-1.5 text-[11px] font-semibold">
                {/* 1. Acknowledge */}
                <button
                  onClick={() => handleStatusUpdate(a.alert_id, "ACKNOWLEDGED", "Officer acknowledged notification")}
                  className="p-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-center border border-slate-700 cursor-pointer"
                >
                  Acknowledge
                </button>

                {/* 2. Alert Bank */}
                <button
                  onClick={() => handleStatusUpdate(a.alert_id, "BANK_ALERTED", "Emergency debit hold transmitted to bank branch")}
                  className="p-1.5 bg-red-950/80 hover:bg-red-900 text-red-300 rounded text-center border border-red-800 cursor-pointer flex items-center justify-center space-x-1"
                >
                  <Send className="w-3 h-3" />
                  <span>Alert Bank</span>
                </button>

                {/* 3. Dispatch Team */}
                <button
                  onClick={() => handleStatusUpdate(a.alert_id, "DISPATCHED", "PCR intercept van deployed to ATM")}
                  className="p-1.5 bg-blue-900/80 hover:bg-blue-800 text-blue-200 rounded text-center border border-blue-700 cursor-pointer flex items-center justify-center space-x-1"
                >
                  <Radio className="w-3 h-3" />
                  <span>Dispatch Team</span>
                </button>

                {/* 4. Monitor Location */}
                <button
                  onClick={() => handleStatusUpdate(a.alert_id, "MONITORING", "CCTV and patrol monitoring activated")}
                  className="p-1.5 bg-purple-950/80 hover:bg-purple-900 text-purple-200 rounded text-center border border-purple-800 cursor-pointer flex items-center justify-center space-x-1"
                >
                  <Bell className="w-3 h-3" />
                  <span>Monitor Location</span>
                </button>

                {/* 5. View Case */}
                <button
                  onClick={() => {
                    setActiveCaseId(a.case_id);
                    navigate("/cases");
                  }}
                  className="p-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded text-center font-bold cursor-pointer flex items-center justify-center space-x-1"
                >
                  <Eye className="w-3 h-3" />
                  <span>View Case</span>
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
