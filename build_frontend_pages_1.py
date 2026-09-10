import os

pages_dir = "/Users/revanth/.gemini/antigravity/scratch/cybertrace-ai/frontend/src/pages"

# 1. Login.tsx
with open(os.path.join(pages_dir, "Login.tsx"), "w") as f:
    f.write('''import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ShieldAlert, Lock, User, CheckCircle2, ArrowRight } from "lucide-react";
import { useApp } from "../context/AppContext";
import { api } from "../services/api";

export const Login: React.FC = () => {
  const [username, setUsername] = useState("demo_officer");
  const [password, setPassword] = useState("CyberTrace@123");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { setUser } = useApp();
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const user = await api.login(username, password);
      setUser(user);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.message || "Invalid Officer ID or Password");
    } finally {
      setLoading(false);
    }
  };

  const autofillDemo = () => {
    setUsername("demo_officer");
    setPassword("CyberTrace@123");
  };

  return (
    <div className="min-h-screen bg-[#070c1b] flex flex-col items-center justify-center p-4">
      {/* Disclaimer Top */}
      <div className="max-w-md w-full mb-6 p-3 bg-slate-900/90 border border-slate-800 rounded-lg text-center text-xs text-slate-400">
        <span className="font-semibold text-amber-400">PROTOTYPE DEMONSTRATION:</span> Synthetic data only. Intended for SIH26184 evaluation.
      </div>

      <div className="max-w-md w-full bg-[#0d142b] border border-slate-800/90 rounded-xl shadow-2xl p-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex p-3 bg-blue-600/20 border border-blue-500/40 rounded-xl text-blue-400 mb-3">
            <ShieldAlert className="w-8 h-8" />
          </div>
          <h1 className="text-2xl font-black tracking-wider text-white">CYBERTRACE AI</h1>
          <p className="text-xs text-slate-400 mt-1 uppercase tracking-widest font-mono">
            Predictive Cybercrime & Cash Withdrawal Intelligence Platform
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-950/80 border border-red-800 rounded text-xs text-red-300 font-medium">
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Officer ID
            </label>
            <div className="relative">
              <User className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="w-full pl-9 pr-3 py-2.5 bg-slate-900/90 border border-slate-700 rounded text-sm text-white focus:outline-none focus:border-blue-500 font-mono"
                placeholder="Officer ID"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Password
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full pl-9 pr-3 py-2.5 bg-slate-900/90 border border-slate-700 rounded text-sm text-white focus:outline-none focus:border-blue-500 font-mono"
                placeholder="Password"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-500 text-white font-semibold text-sm rounded shadow-lg transition-colors flex items-center justify-center space-x-2 cursor-pointer disabled:opacity-50"
          >
            <span>{loading ? "Authenticating..." : "Access Intelligence Console"}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        {/* Demo Credentials Helper */}
        <div className="mt-6 pt-5 border-t border-slate-800 text-center">
          <div className="text-[11px] text-slate-400 mb-2 font-mono">
            Demo Credentials: <span className="text-white font-bold">demo_officer</span> / <span className="text-white font-bold">CyberTrace@123</span>
          </div>
          <button
            type="button"
            onClick={autofillDemo}
            className="text-xs text-blue-400 hover:text-blue-300 underline font-medium cursor-pointer"
          >
            Auto-fill Demo Credentials
          </button>
        </div>
      </div>
    </div>
  );
};
''')

# 2. Dashboard.tsx
with open(os.path.join(pages_dir, "Dashboard.tsx"), "w") as f:
    f.write('''import React, { useEffect, useState } from "react";
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
''')

# 3. Cases.tsx
with open(os.path.join(pages_dir, "Cases.tsx"), "w") as f:
    f.write('''import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  FolderSearch, User, Phone, MapPin, IndianRupee, ShieldAlert,
  Send, Bell, Radio, CheckCircle, FileText, RefreshCw, Clock
} from "lucide-react";
import { useApp } from "../context/AppContext";
import { StatusBadge } from "../components/StatusBadge";
import { api } from "../services/api";
import { CaseDetail } from "../types";

export const Cases: React.FC = () => {
  const { activeCaseId, setActiveCaseId, updateCaseStatus, cases } = useApp();
  const [detail, setDetail] = useState<CaseDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const loadCase = async (id: string) => {
    setLoading(true);
    try {
      const data = await api.getCaseDetail(id);
      setDetail(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeCaseId) {
      loadCase(activeCaseId);
    }
  }, [activeCaseId]);

  const handleAction = async (actionType: string, desc: string, targetStatus?: string) => {
    if (!activeCaseId) return;
    try {
      await api.addCaseAction(activeCaseId, actionType, desc);
      if (targetStatus) {
        await updateCaseStatus(targetStatus, desc);
      }
      await loadCase(activeCaseId);
    } catch (e) {
      console.error(e);
    }
  };

  const lifecycle = [
    "NEW",
    "UNDER ANALYSIS",
    "HIGH-RISK PREDICTION",
    "ALERT GENERATED",
    "ACTION INITIATED",
    "MONITORING",
    "RESOLVED"
  ];

  const currentStatusIndex = detail ? lifecycle.indexOf(detail.case.status) : 0;

  return (
    <div className="p-6 space-y-6">
      {/* Top Selector & Quick stats */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-xl font-black text-white flex items-center space-x-2">
            <FolderSearch className="w-5 h-5 text-blue-400" />
            <span>Cybercrime Case Investigation Dossier</span>
          </h1>
          <p className="text-xs text-slate-400">
            Case Profile, Incident Vector, Action Directives, and Dynamic Chain of Custody
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <select
            value={activeCaseId}
            onChange={(e) => setActiveCaseId(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-white text-xs font-mono rounded px-3 py-1.5 focus:outline-none focus:border-blue-500 cursor-pointer"
          >
            {cases.map((c) => (
              <option key={c.case_id} value={c.case_id}>
                {c.case_id} &bull; {c.fraud_type} ({c.risk_level})
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading || !detail ? (
        <div className="p-12 text-center text-slate-400 text-sm">Loading case intelligence dossier...</div>
      ) : (
        <>
          {/* Status Lifecycle Stepper */}
          <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-4">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3">
              Case Operational Lifecycle
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-7 gap-2">
              {lifecycle.map((st, idx) => {
                const isPassed = idx <= currentStatusIndex;
                const isCurrent = idx === currentStatusIndex;
                return (
                  <button
                    key={st}
                    onClick={() => handleAction("Status Updated", `Officer transitioned case status to ${st}.`, st)}
                    className={`p-2 rounded text-center text-[10px] font-mono font-bold transition-all border cursor-pointer ${
                      isCurrent
                        ? "bg-blue-600 text-white border-blue-400 shadow-md ring-2 ring-blue-500/50"
                        : isPassed
                        ? "bg-blue-950/60 text-blue-300 border-blue-800"
                        : "bg-slate-900 text-slate-500 border-slate-800 hover:border-slate-700"
                    }`}
                  >
                    <div>STEP {idx + 1}</div>
                    <div className="truncate mt-0.5">{st}</div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Case Dossier Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Complainant & Incident Profile */}
            <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-5 space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <h3 className="text-sm font-bold text-white">Complainant Information</h3>
                <StatusBadge type="risk" value={detail.case.risk_level} />
              </div>

              <div className="space-y-2.5 text-xs">
                <div className="flex items-center justify-between">
                  <span className="text-slate-400 flex items-center space-x-1.5"><User className="w-3.5 h-3.5 text-slate-500" /><span>Complainant</span></span>
                  <span className="font-semibold text-white">{detail.case.victim_name}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400 flex items-center space-x-1.5"><Phone className="w-3.5 h-3.5 text-slate-500" /><span>Contact Phone</span></span>
                  <span className="font-mono text-slate-300">{detail.case.victim_phone}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400 flex items-center space-x-1.5"><MapPin className="w-3.5 h-3.5 text-slate-500" /><span>Origin Jurisdiction</span></span>
                  <span className="text-slate-300">{detail.case.victim_location}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400 flex items-center space-x-1.5"><IndianRupee className="w-3.5 h-3.5 text-slate-500" /><span>Defrauded Loss</span></span>
                  <span className="font-mono font-bold text-red-400 text-sm">₹{detail.case.amount.toLocaleString()}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Portal Reference</span>
                  <span className="font-mono text-blue-400">{detail.complaint?.portal_ref || "NCRP-2026-8921-KA"}</span>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-800">
                <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
                  Incident Synopsis
                </div>
                <p className="text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-3 rounded border border-slate-800/80">
                  {detail.case.summary}
                </p>
              </div>

              {/* Action Buttons Toolbar */}
              <div className="pt-3 border-t border-slate-800">
                <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2">
                  Direct Intervention Controls
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    onClick={() => handleAction("Bank Alert Issued", "Issued formal debit freeze directive under Section 102 CrPC to nodal bank.")}
                    className="p-2 bg-red-950/80 hover:bg-red-900 border border-red-700/80 text-red-300 rounded text-xs font-bold transition-colors cursor-pointer flex items-center justify-center space-x-1"
                  >
                    <Send className="w-3.5 h-3.5" />
                    <span>ALERT BANK</span>
                  </button>

                  <button
                    onClick={() => handleAction("Field Patrol Dispatched", "Dispatched mobile intercept team to ATM perimeter.", "ACTION INITIATED")}
                    className="p-2 bg-blue-900/80 hover:bg-blue-800 border border-blue-600 text-blue-200 rounded text-xs font-bold transition-colors cursor-pointer flex items-center justify-center space-x-1"
                  >
                    <Radio className="w-3.5 h-3.5" />
                    <span>DISPATCH TEAM</span>
                  </button>

                  <button
                    onClick={() => handleAction("ATM Surveillance Activated", "Designated ATM flagged for CCTV and field perimeter monitoring.", "MONITORING")}
                    className="p-2 bg-purple-950/80 hover:bg-purple-900 border border-purple-700 text-purple-200 rounded text-xs font-bold transition-colors cursor-pointer flex items-center justify-center space-x-1"
                  >
                    <Bell className="w-3.5 h-3.5" />
                    <span>MONITOR ATM</span>
                  </button>

                  <button
                    onClick={() => navigate("/reports")}
                    className="p-2 bg-emerald-950/80 hover:bg-emerald-900 border border-emerald-700 text-emerald-300 rounded text-xs font-bold transition-colors cursor-pointer flex items-center justify-center space-x-1"
                  >
                    <FileText className="w-3.5 h-3.5" />
                    <span>GENERATE REPORT</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Predictive Intelligence & Forecasted Cash-out */}
            <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-5 space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <h3 className="text-sm font-bold text-white">Forecasted Cash-Out Point</h3>
                <span className="font-mono text-xs text-blue-400 font-bold">{detail.case.risk_score}% PROBABILITY</span>
              </div>

              <div className="p-4 bg-gradient-to-br from-rose-950/40 to-slate-900 border border-rose-900/60 rounded-lg space-y-2">
                <div className="text-[10px] uppercase font-bold text-rose-400 tracking-wider">Target Terminal</div>
                <div className="text-base font-black text-white">{detail.case.predicted_atm_name}</div>
                <div className="flex items-center justify-between text-xs pt-2 border-t border-rose-900/40">
                  <span className="text-slate-400">Time Window:</span>
                  <span className="font-mono font-bold text-amber-400">{detail.case.predicted_time_window}</span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-400">Predicted Amount:</span>
                  <span className="font-mono font-bold text-white">₹{detail.case.predicted_amount.toLocaleString()}</span>
                </div>
              </div>

              <div className="space-y-2 pt-2">
                <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                  Recommended Investigative Protocol
                </div>
                <ul className="text-xs text-slate-300 space-y-2 list-disc list-inside bg-slate-900/60 p-3 rounded border border-slate-800/80">
                  <li>Initiate nodal contact with bank security cell for immediate transaction pause.</li>
                  <li>Coordinate with jurisdictional station patrol for physical kiosk surveillance.</li>
                  <li>Preserve IP, IMSI and CDR logs from payment gateway intermediary hops.</li>
                </ul>
              </div>

              <div className="pt-2 flex space-x-2">
                <button
                  onClick={() => navigate("/predict")}
                  className="flex-1 py-2 bg-blue-600/30 border border-blue-500/50 hover:bg-blue-600 hover:text-white text-blue-300 rounded text-xs font-semibold text-center transition-colors cursor-pointer"
                >
                  View Full AI Breakdown &rarr;
                </button>
                <button
                  onClick={() => navigate("/map")}
                  className="flex-1 py-2 bg-purple-600/30 border border-purple-500/50 hover:bg-purple-600 hover:text-white text-purple-300 rounded text-xs font-semibold text-center transition-colors cursor-pointer"
                >
                  View on Bengaluru Map &rarr;
                </button>
              </div>
            </div>

            {/* Case Action Timeline */}
            <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-5 flex flex-col">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
                <h3 className="text-sm font-bold text-white flex items-center space-x-2">
                  <Clock className="w-4 h-4 text-blue-400" />
                  <span>Chain of Custody & Action Log</span>
                </h3>
                <span className="text-[10px] font-mono text-slate-500">{detail.timeline.length} Records</span>
              </div>

              <div className="space-y-3 overflow-y-auto max-h-[380px] custom-scrollbar pr-1 flex-1">
                {detail.timeline.map((act) => (
                  <div key={act.id} className="relative pl-5 pb-3 border-l-2 border-slate-800 last:border-l-0 text-xs">
                    <span className="absolute -left-[5px] top-0.5 w-2 h-2 rounded-full bg-blue-500"></span>
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-white">{act.action_type}</span>
                      <span className="font-mono text-[10px] text-slate-500">
                        {new Date(act.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                    <p className="text-slate-400 text-[11px] mt-0.5 leading-relaxed">{act.description}</p>
                    <span className="text-[10px] font-mono text-slate-500 block mt-1">
                      Logged by: {act.officer_id}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
''')

# 4. Ingestion.tsx
with open(os.path.join(pages_dir, "Ingestion.tsx"), "w") as f:
    f.write('''import React, { useEffect, useState } from "react";
import {
  Database, UploadCloud, RefreshCw, FileSpreadsheet, CheckCircle2,
  ShieldCheck, AlertCircle, ArrowRight
} from "lucide-react";
import { api } from "../services/api";
import { IngestionStats, Transaction } from "../types";
import { useApp } from "../context/AppContext";

export const Ingestion: React.FC = () => {
  const [stats, setStats] = useState<IngestionStats | null>(null);
  const [processing, setProcessing] = useState(false);
  const [sampleTxs, setSampleTxs] = useState<Transaction[]>([]);
  const { refreshCases, refreshAlerts } = useApp();

  const loadStats = async () => {
    try {
      const data = await api.getIngestionStats();
      setStats(data);
      const txs = await api.getTransactions("CYB-1024");
      setSampleTxs(txs);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadStats();
  }, []);

  const handleProcess = async () => {
    setProcessing(true);
    try {
      await api.processData();
      await loadStats();
      await refreshCases();
      await refreshAlerts();
    } catch (e) {
      console.error(e);
    } finally {
      setProcessing(false);
    }
  };

  const handleReset = async () => {
    setProcessing(true);
    try {
      await api.resetDemoData();
      await loadStats();
      await refreshCases();
      await refreshAlerts();
    } catch (e) {
      console.error(e);
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-xl font-black text-white flex items-center space-x-2">
            <Database className="w-5 h-5 text-blue-400" />
            <span>Data Ingestion & Pre-Processing Engine</span>
          </h1>
          <p className="text-xs text-slate-400">
            Multi-source ingestion pipeline: National Cybercrime Portal, Banking Feeds, KYC Registries & Threat Feeds
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleReset}
            disabled={processing}
            className="px-3.5 py-2 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-semibold flex items-center space-x-1.5 transition-colors cursor-pointer"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${processing ? "animate-spin" : ""}`} />
            <span>Load Demo Dataset</span>
          </button>

          <button
            onClick={handleProcess}
            disabled={processing}
            className="px-3.5 py-2 rounded bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold flex items-center space-x-1.5 shadow-md transition-colors cursor-pointer"
          >
            <UploadCloud className="w-3.5 h-3.5" />
            <span>{processing ? "Processing Pipeline..." : "Execute Processing Pipeline"}</span>
          </button>
        </div>
      </div>

      {/* 4 Ingestion Sources Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-4 space-y-2">
          <div className="text-[10px] font-mono text-blue-400 uppercase font-bold tracking-wider">Source Type 01</div>
          <h3 className="text-sm font-bold text-white">Cybercrime Complaints</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Direct ingestion from NCRP portal, 1930 helpline records, and state FIR databases.
          </p>
          <div className="pt-2 flex items-center justify-between text-[11px] font-mono border-t border-slate-800 text-slate-400">
            <span>Status: <span className="text-emerald-400 font-bold">CONNECTED</span></span>
            <span>59 Cases</span>
          </div>
        </div>

        <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-4 space-y-2">
          <div className="text-[10px] font-mono text-purple-400 uppercase font-bold tracking-wider">Source Type 02</div>
          <h3 className="text-sm font-bold text-white">Bank Transaction Data</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Real-time IMPS, NEFT, RTGS, and UPI switch logs via Indian Cyber Crime Coordination Centre (I4C).
          </p>
          <div className="pt-2 flex items-center justify-between text-[11px] font-mono border-t border-slate-800 text-slate-400">
            <span>Status: <span className="text-emerald-400 font-bold">STREAMING</span></span>
            <span>530 Txns</span>
          </div>
        </div>

        <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-4 space-y-2">
          <div className="text-[10px] font-mono text-amber-400 uppercase font-bold tracking-wider">Source Type 03</div>
          <h3 className="text-sm font-bold text-white">KYC / Account Info</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Core Banking System (CBS) profile extracts, mule account indicators, and branch linkage.
          </p>
          <div className="pt-2 flex items-center justify-between text-[11px] font-mono border-t border-slate-800 text-slate-400">
            <span>Status: <span className="text-emerald-400 font-bold">VALIDATED</span></span>
            <span>59 Accounts</span>
          </div>
        </div>

        <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-4 space-y-2">
          <div className="text-[10px] font-mono text-red-400 uppercase font-bold tracking-wider">Source Type 04</div>
          <h3 className="text-sm font-bold text-white">External Threat Intel</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Known mule syndicate phone numbers, suspect IP blocks, and dark web fraud forum dumps.
          </p>
          <div className="pt-2 flex items-center justify-between text-[11px] font-mono border-t border-slate-800 text-slate-400">
            <span>Status: <span className="text-emerald-400 font-bold">ACTIVE SYNC</span></span>
            <span>22 ATM Zones</span>
          </div>
        </div>
      </div>

      {/* Processing Pipeline Diagram */}
      <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-5">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-4">
          Data Processing Pipeline Architecture
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-6 gap-2">
          {[
            { step: "RAW DATA", desc: "Batch & Stream Ingestion", stat: "650+ records" },
            { step: "CLEANING", desc: "Missing Value Handling", stat: "100% complete" },
            { step: "NORMALIZATION", desc: "Timestamp & INR Uniformity", stat: "Duplicates: 14" },
            { step: "FEATURE ENG", desc: "Velocity & Decay Matrices", stat: "9 ML Vectors" },
            { step: "GRAPH SYNTHESIS", desc: "Mule Hop Linkage", stat: "Multi-hop DAG" },
            { step: "MODEL-READY", desc: "Inference Deployment", stat: "Active Engine" },
          ].map((s, idx) => (
            <div key={s.step} className="p-3 bg-slate-900 border border-slate-800 rounded text-center">
              <div className="text-[10px] font-mono font-bold text-blue-400">{s.step}</div>
              <div className="text-xs text-slate-300 font-semibold mt-1">{s.desc}</div>
              <div className="text-[10px] font-mono text-emerald-400 mt-2">{s.stat}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Ingestion Statistics Cards */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="bg-slate-900/90 border border-slate-800 p-3 rounded text-center">
            <span className="text-[10px] text-slate-400 uppercase font-mono">Records Received</span>
            <div className="text-lg font-bold text-white font-mono">{stats.records_received}</div>
          </div>
          <div className="bg-slate-900/90 border border-slate-800 p-3 rounded text-center">
            <span className="text-[10px] text-slate-400 uppercase font-mono">Processed</span>
            <div className="text-lg font-bold text-emerald-400 font-mono">{stats.records_processed}</div>
          </div>
          <div className="bg-slate-900/90 border border-slate-800 p-3 rounded text-center">
            <span className="text-[10px] text-slate-400 uppercase font-mono">Duplicates Removed</span>
            <div className="text-lg font-bold text-amber-400 font-mono">{stats.duplicates_removed}</div>
          </div>
          <div className="bg-slate-900/90 border border-slate-800 p-3 rounded text-center">
            <span className="text-[10px] text-slate-400 uppercase font-mono">Suspicious Accounts</span>
            <div className="text-lg font-bold text-red-400 font-mono">{stats.suspicious_accounts}</div>
          </div>
          <div className="bg-slate-900/90 border border-slate-800 p-3 rounded text-center">
            <span className="text-[10px] text-slate-400 uppercase font-mono">Suspicious Txns</span>
            <div className="text-lg font-bold text-rose-400 font-mono">{stats.suspicious_transactions}</div>
          </div>
        </div>
      )}

      {/* Ingested Dataset Preview Table */}
      <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-5">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-bold text-white">Ingested Bank Transaction Feed Preview</h3>
            <p className="text-xs text-slate-400">Sample raw transactional telemetry before ML vectorization</p>
          </div>
          <span className="text-xs font-mono text-slate-500">Case: CYB-1024 Feed</span>
        </div>

        <div className="overflow-x-auto custom-scrollbar">
          <table className="w-full text-left text-xs border-collapse font-mono">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 text-[11px]">
                <th className="pb-2">Transaction ID</th>
                <th className="pb-2">Source Account</th>
                <th className="pb-2">Destination Account</th>
                <th className="pb-2">Amount</th>
                <th className="pb-2">Channel</th>
                <th className="pb-2">IP Address</th>
                <th className="pb-2">Device ID</th>
                <th className="pb-2">Risk</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {sampleTxs.map((t) => (
                <tr key={t.transaction_id} className="hover:bg-slate-800/30">
                  <td className="py-2.5 text-blue-400 font-bold">{t.transaction_id}</td>
                  <td className="py-2.5">{t.source_account}</td>
                  <td className="py-2.5">{t.destination_account}</td>
                  <td className="py-2.5 font-bold text-white">₹{t.amount.toLocaleString()}</td>
                  <td className="py-2.5">{t.channel || t.transaction_type}</td>
                  <td className="py-2.5 text-slate-400">{t.ip_address}</td>
                  <td className="py-2.5 text-slate-500">{t.device_id}</td>
                  <td className="py-2.5">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      t.risk_indicator === "HIGH" ? "bg-red-950 text-red-400 border border-red-800" : "bg-amber-950 text-amber-400 border border-amber-800"
                    }`}>
                      {t.risk_indicator}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
''')

# 5. Transactions.tsx
with open(os.path.join(pages_dir, "Transactions.tsx"), "w") as f:
    f.write('''import React, { useEffect, useState } from "react";
import { GitFork, ShieldAlert, AlertTriangle, ArrowRight, UserCheck, RefreshCw } from "lucide-react";
import { useApp } from "../context/AppContext";
import { api } from "../services/api";
import { TransactionGraphData, Transaction } from "../types";
import { TransactionGraph } from "../components/TransactionGraph";

export const Transactions: React.FC = () => {
  const { activeCaseId, cases, setActiveCaseId } = useApp();
  const [graphData, setGraphData] = useState<TransactionGraphData | null>(null);
  const [txs, setTxs] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(false);

  const loadData = async (caseId: string) => {
    setLoading(true);
    try {
      const g = await api.getTransactionGraph(caseId);
      setGraphData(g);
      const t = await api.getTransactions(caseId);
      setTxs(t);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeCaseId) {
      loadData(activeCaseId);
    }
  }, [activeCaseId]);

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-xl font-black text-white flex items-center space-x-2">
            <GitFork className="w-5 h-5 text-blue-400" />
            <span>Transaction Intelligence & Money Trail Graph</span>
          </h1>
          <p className="text-xs text-slate-400">
            Multi-hop forensic tracing from victim debit to final mule liquidity node
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <select
            value={activeCaseId}
            onChange={(e) => setActiveCaseId(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-white text-xs font-mono rounded px-3 py-1.5 focus:outline-none focus:border-blue-500 cursor-pointer"
          >
            {cases.map((c) => (
              <option key={c.case_id} value={c.case_id}>
                {c.case_id} &bull; {c.fraud_type}
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading || !graphData ? (
        <div className="p-12 text-center text-slate-400 text-sm">Loading transaction intelligence network...</div>
      ) : (
        <>
          {/* Interactive Network Visualizer */}
          <div className="h-[380px]">
            <TransactionGraph data={graphData} />
          </div>

          {/* Raw Transactions Table */}
          <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-5">
            <h3 className="text-sm font-bold text-white mb-3">Case Transaction Trail Telemetry</h3>
            <div className="overflow-x-auto custom-scrollbar">
              <table className="w-full text-left text-xs border-collapse font-mono">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 text-[11px]">
                    <th className="pb-2">Tx ID</th>
                    <th className="pb-2">Timestamp</th>
                    <th className="pb-2">From Account</th>
                    <th className="pb-2">To Account</th>
                    <th className="pb-2">Amount</th>
                    <th className="pb-2">Channel</th>
                    <th className="pb-2">Location Hub</th>
                    <th className="pb-2">Layer</th>
                    <th className="pb-2">Flag</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-slate-200">
                  {txs.map((t) => (
                    <tr key={t.transaction_id} className="hover:bg-slate-800/30">
                      <td className="py-2.5 font-bold text-blue-400">{t.transaction_id}</td>
                      <td className="py-2.5 text-slate-400">{new Date(t.timestamp).toLocaleTimeString()}</td>
                      <td className="py-2.5">{t.source_account}</td>
                      <td className="py-2.5 text-amber-300">{t.destination_account}</td>
                      <td className="py-2.5 font-bold text-white">₹{t.amount.toLocaleString()}</td>
                      <td className="py-2.5">{t.channel || t.transaction_type}</td>
                      <td className="py-2.5 text-slate-400">{t.location}</td>
                      <td className="py-2.5 font-bold">Layer {t.layer_depth}</td>
                      <td className="py-2.5">
                        {t.is_suspicious ? (
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-red-950 text-red-400 border border-red-800">
                            SUSPICIOUS
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-400">
                            NORMAL
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
''')

print("Pages 1 (Login, Dashboard, Cases, Ingestion, Transactions) created successfully.")
