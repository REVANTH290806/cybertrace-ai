import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  FolderSearch, IndianRupee, AlertOctagon, MapPin,
  BellRing, ArrowUpRight, TrendingUp, CheckCircle, ShieldCheck, Activity
} from "lucide-react";
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid
} from "recharts";
import { useApp } from "../context/AppContext";
import { StatusBadge } from "../components/StatusBadge";
import { api } from "../services/api";
import { AnalyticsData } from "../types";

export const Dashboard: React.FC = () => {
  const { cases, alerts, setActiveCaseId, refreshAlerts } = useApp();
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    api.getAnalytics().then(setAnalytics).catch(console.error);
  }, []);

  const handleCaseSelect = (caseId: string) => {
    setActiveCaseId(caseId);
    navigate("/cases");
  };

  const handleAcknowledgeAlert = async (alertId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await api.updateAlertStatus(alertId, "ACKNOWLEDGED");
      await refreshAlerts();
    } catch (err) {
      console.error(err);
    }
  };

  const recentCases = cases.slice(0, 7);
  const recentAlerts = alerts.slice(0, 5);

  return (
    <div className="p-6 space-y-6">
      {/* Top Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {/* Active Cases */}
        <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-4">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase">
            <span>Active Cases</span>
            <FolderSearch className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-extrabold text-white mt-2 font-mono">124</div>
          <div className="text-[11px] text-emerald-400 mt-1 flex items-center">
            <ArrowUpRight className="w-3 h-3 mr-0.5" /> +12% this week
          </div>
        </div>

        {/* Amount Under Investigation */}
        <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-4">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase">
            <span>Under Investigation</span>
            <IndianRupee className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-extrabold text-white mt-2 font-mono">₹38.6 Cr</div>
          <div className="text-[11px] text-slate-400 mt-1">Total reported loss pool</div>
        </div>

        {/* High-Risk Cases */}
        <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-4">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase">
            <span>High-Risk Cases</span>
            <AlertOctagon className="w-4 h-4 text-red-400" />
          </div>
          <div className="text-2xl font-extrabold text-red-400 mt-2 font-mono">17</div>
          <div className="text-[11px] text-red-400/80 mt-1">Imminent cash-out threat</div>
        </div>

        {/* Predicted Withdrawals */}
        <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-4">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase">
            <span>Predicted Withdrawals</span>
            <MapPin className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-extrabold text-purple-300 mt-2 font-mono">42</div>
          <div className="text-[11px] text-purple-400 mt-1">Within 2 to 4 hour windows</div>
        </div>

        {/* Preventive Alerts */}
        <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-4">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase">
            <span>Preventive Alerts</span>
            <BellRing className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-extrabold text-emerald-400 mt-2 font-mono">18</div>
          <div className="text-[11px] text-emerald-400 mt-1">Field intercepts triggered</div>
        </div>
      </div>

      {/* Main Grid: Cases Table + Right Column (Trend & Alerts) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Recent Cases Table */}
        <div className="lg:col-span-2 bg-[#0e162f] border border-slate-800 rounded-lg p-5 flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-base font-bold text-white">Active Cybercrime Investigation Queue</h2>
              <p className="text-xs text-slate-400">Cases under predictive cash withdrawal tracking</p>
            </div>
            <button
              onClick={() => navigate("/cases")}
              className="text-xs text-blue-400 hover:text-blue-300 font-semibold cursor-pointer"
            >
              View All Cases &rarr;
            </button>
          </div>

          <div className="overflow-x-auto custom-scrollbar flex-1">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 font-mono text-[11px]">
                  <th className="pb-2.5">Case ID</th>
                  <th className="pb-2.5">Fraud Type</th>
                  <th className="pb-2.5">Amount</th>
                  <th className="pb-2.5">Status</th>
                  <th className="pb-2.5">Risk</th>
                  <th className="pb-2.5">Predicted Location</th>
                  <th className="pb-2.5 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-medium text-slate-200">
                {recentCases.map((c) => (
                  <tr
                    key={c.case_id}
                    onClick={() => handleCaseSelect(c.case_id)}
                    className="hover:bg-slate-800/40 cursor-pointer transition-colors"
                  >
                    <td className="py-3 font-mono font-bold text-blue-400">{c.case_id}</td>
                    <td className="py-3">{c.fraud_type}</td>
                    <td className="py-3 font-mono">₹{c.amount.toLocaleString()}</td>
                    <td className="py-3"><StatusBadge type="status" value={c.status} /></td>
                    <td className="py-3"><StatusBadge type="risk" value={c.risk_level} /></td>
                    <td className="py-3 font-mono text-slate-300 truncate max-w-[140px]">{c.predicted_atm_name || "Scanning..."}</td>
                    <td className="py-3 text-right">
                      <span className="text-blue-400 hover:text-blue-300 text-[11px] underline">Investigate</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right 1 Col: Trend Chart & Prediction Summary */}
        <div className="space-y-6">
          {/* Cybercrime Trend Chart */}
          <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-5">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-bold text-white flex items-center space-x-1.5">
                <TrendingUp className="w-4 h-4 text-blue-400" />
                <span>Cybercrime Incident Velocity</span>
              </h3>
              <span className="text-[10px] font-mono text-slate-400">Weekly Pool</span>
            </div>
            <div className="h-44 w-full">
              {analytics ? (
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={analytics.timeline_trend}>
                    <defs>
                      <linearGradient id="caseGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4} />
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="period" stroke="#64748b" fontSize={10} />
                    <YAxis stroke="#64748b" fontSize={10} />
                    <Tooltip
                      contentStyle={{ backgroundColor: "#090e1f", borderColor: "#334155", fontSize: 11 }}
                    />
                    <Area type="monotone" dataKey="cases" stroke="#3b82f6" fillOpacity={1} fill="url(#caseGradient)" />
                  </AreaChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex items-center justify-center text-xs text-slate-500">Loading trend...</div>
              )}
            </div>
          </div>

          {/* Prediction Summary */}
          <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-5">
            <h3 className="text-sm font-bold text-white mb-3">Prediction Summary</h3>
            <div className="space-y-2.5 text-xs">
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <span className="text-slate-400">High-Risk ATM Terminals</span>
                <span className="font-mono font-bold text-red-400">6 Hotspots</span>
              </div>
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <span className="text-slate-400">Predicted Cash Outflows</span>
                <span className="font-mono font-bold text-white">42 Forecasts</span>
              </div>
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <span className="text-slate-400">Average Confidence Score</span>
                <span className="font-mono font-bold text-emerald-400">84.6%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-400">Amount at Imminent Risk</span>
                <span className="font-mono font-bold text-amber-400">₹71.2 Lakhs</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Row: Recent Alerts + System Health Status */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Alerts Feed (2 cols) */}
        <div className="lg:col-span-2 bg-[#0e162f] border border-slate-800 rounded-lg p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-white flex items-center space-x-2">
              <BellRing className="w-4 h-4 text-red-400" />
              <span>Real-Time Predictive Intercept Alerts</span>
            </h3>
            <button onClick={() => navigate("/alerts")} className="text-xs text-blue-400 hover:text-blue-300 cursor-pointer">
              Manage All Alerts &rarr;
            </button>
          </div>

          <div className="space-y-2.5">
            {recentAlerts.map((a) => (
              <div
                key={a.alert_id}
                className="flex items-center justify-between p-3 bg-slate-900/80 border border-slate-800 rounded-md text-xs hover:border-slate-700 transition-colors"
              >
                <div className="flex items-center space-x-3">
                  <span className="px-2 py-0.5 rounded font-bold text-[10px] bg-red-950 text-red-400 border border-red-800">
                    {a.severity}
                  </span>
                  <div>
                    <div className="font-bold text-white">
                      {a.case_id} &bull; <span className="text-slate-300">{a.location_name || a.location_id}</span>
                    </div>
                    <div className="text-[11px] text-slate-400 font-mono">
                      Probability: <span className="text-red-400 font-bold">{a.probability}%</span> &bull; Window: {a.expected_time} &bull; Amount: ₹{a.amount.toLocaleString()}
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  {a.status === "ACTIVE" ? (
                    <button
                      onClick={(e) => handleAcknowledgeAlert(a.alert_id, e)}
                      className="px-2.5 py-1 rounded bg-blue-600/30 border border-blue-500/50 text-blue-300 hover:bg-blue-600 hover:text-white transition-colors cursor-pointer text-[11px] font-medium"
                    >
                      Acknowledge
                    </button>
                  ) : (
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-800 text-slate-400">
                      {a.status}
                    </span>
                  )}
                  <button
                    onClick={() => {
                      setActiveCaseId(a.case_id);
                      navigate("/cases");
                    }}
                    className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-[11px] cursor-pointer"
                  >
                    View Case
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* System Status Indicators (1 col) */}
        <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-5">
          <h3 className="text-sm font-bold text-white mb-3 flex items-center space-x-2">
            <Activity className="w-4 h-4 text-emerald-400" />
            <span>Infrastructure Health</span>
          </h3>

          <div className="space-y-3 text-xs">
            <div className="flex items-center justify-between p-2 bg-slate-900/60 rounded border border-slate-800">
              <span className="text-slate-300">Data Ingestion Feed</span>
              <span className="flex items-center space-x-1 text-emerald-400 font-mono text-[11px]">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>ONLINE / HEALTHY</span>
              </span>
            </div>

            <div className="flex items-center justify-between p-2 bg-slate-900/60 rounded border border-slate-800">
              <span className="text-slate-300">AI Predictive Engine</span>
              <span className="flex items-center space-x-1 text-emerald-400 font-mono text-[11px]">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>ONLINE (100 TREES)</span>
              </span>
            </div>

            <div className="flex items-center justify-between p-2 bg-slate-900/60 rounded border border-slate-800">
              <span className="text-slate-300">Intelligence DB (SQLite/PG)</span>
              <span className="flex items-center space-x-1 text-emerald-400 font-mono text-[11px]">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>CONNECTED</span>
              </span>
            </div>

            <div className="flex items-center justify-between p-2 bg-slate-900/60 rounded border border-slate-800">
              <span className="text-slate-300">Real-Time Alert Dispatch</span>
              <span className="flex items-center space-x-1 text-emerald-400 font-mono text-[11px]">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>ACTIVE</span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
