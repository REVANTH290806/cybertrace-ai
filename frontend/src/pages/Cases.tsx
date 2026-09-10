import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  FolderSearch, User, Phone, MapPin, IndianRupee, ShieldAlert,
  Send, Bell, Radio, CheckCircle, FileText, RefreshCw, Clock,
  Edit3, AlertTriangle, X
} from "lucide-react";
import { useApp } from "../context/AppContext";
import { StatusBadge } from "../components/StatusBadge";
import { api } from "../services/api";
import { CaseDetail } from "../types";

export const Cases: React.FC = () => {
  const { activeCaseId, setActiveCaseId, updateCaseStatus, cases, refreshCases } = useApp();
  const [detail, setDetail] = useState<CaseDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<string | null>(null);
  const [showUpdateModal, setShowUpdateModal] = useState(false);
  const [modalStatus, setModalStatus] = useState("UNDER ANALYSIS");
  const [modalNotes, setModalNotes] = useState("");
  const navigate = useNavigate();

  const showFeedback = (msg: string) => {
    setToast(msg);
    setTimeout(() => setToast(null), 4000);
  };

  const loadCase = async (id: string) => {
    setLoading(true);
    try {
      const data = await api.getCaseDetail(id);
      setDetail(data);
      if (data?.case) {
        setModalStatus(data.case.status);
      }
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
      await refreshCases();
      showFeedback(`Action Executed: ${actionType}`);
    } catch (e) {
      console.error(e);
      showFeedback(`Failed to record action: ${actionType}`);
    }
  };

  const handleModalSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeCaseId) return;
    const desc = modalNotes.trim() || `Officer updated case status to ${modalStatus}.`;
    await handleAction("Manual Case Update", desc, modalStatus);
    setShowUpdateModal(false);
    setModalNotes("");
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

      {toast && (
        <div className="p-3 bg-blue-950/90 border border-blue-500 text-blue-200 rounded text-xs font-semibold flex items-center justify-between shadow-lg">
          <div className="flex items-center space-x-2">
            <CheckCircle className="w-4 h-4 text-emerald-400" />
            <span>{toast}</span>
          </div>
          <button onClick={() => setToast(null)} className="text-slate-400 hover:text-white cursor-pointer">&times;</button>
        </div>
      )}

      {loading || !detail ? (
        <div className="p-12 text-center text-slate-400 text-sm">Loading case intelligence dossier...</div>
      ) : (
        <>
          {/* Status Lifecycle Stepper */}
          <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                Case Operational Lifecycle (Click any step to transition)
              </h3>
              <span className="text-xs font-mono text-blue-400 font-bold">
                Current: {detail.case.status}
              </span>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-7 gap-2">
              {lifecycle.map((st, idx) => {
                const isPassed = idx <= currentStatusIndex;
                const isCurrent = idx === currentStatusIndex;
                return (
                  <button
                    key={st}
                    onClick={() => handleAction("Status Transition", `Officer transitioned case status to ${st}.`, st)}
                    className={`p-2.5 rounded text-center text-[10px] font-mono font-bold transition-all border cursor-pointer ${
                      isCurrent
                        ? "bg-blue-600 text-white border-blue-400 shadow-md ring-2 ring-blue-500/50 scale-102"
                        : isPassed
                        ? "bg-blue-950/70 text-blue-300 border-blue-800 hover:bg-blue-900/60"
                        : "bg-slate-900 text-slate-500 border-slate-800 hover:border-slate-700 hover:text-slate-300"
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

              {/* Action Buttons Toolbar - ALL 6 BUTTONS REQUIRED BY SECTION 16 */}
              <div className="pt-3 border-t border-slate-800">
                <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2">
                  Direct Intervention Controls (Section 16 Directives)
                </div>
                <div className="grid grid-cols-2 gap-2">
                  {/* 1. ALERT BANK */}
                  <button
                    onClick={() => handleAction("Section 102 Freeze Directive Issued", "Issued formal debit freeze directive under Section 102 CrPC to beneficiary banks.")}
                    className="p-2.5 bg-red-950/80 hover:bg-red-900 border border-red-700/80 text-red-300 rounded text-xs font-bold transition-colors cursor-pointer flex items-center justify-center space-x-1 shadow"
                  >
                    <Send className="w-3.5 h-3.5" />
                    <span>ALERT BANK</span>
                  </button>

                  {/* 2. DISPATCH FIELD TEAM */}
                  <button
                    onClick={() => handleAction("Mobile Intercept Unit Dispatched", "Dispatched mobile intercept team to ATM perimeter for physical surveillance.", "ACTION INITIATED")}
                    className="p-2.5 bg-blue-900/80 hover:bg-blue-800 border border-blue-600 text-blue-200 rounded text-xs font-bold transition-colors cursor-pointer flex items-center justify-center space-x-1 shadow"
                  >
                    <Radio className="w-3.5 h-3.5" />
                    <span>DISPATCH FIELD TEAM</span>
                  </button>

                  {/* 3. MONITOR ATM */}
                  <button
                    onClick={() => handleAction("ATM Surveillance Activated", "Designated ATM flagged for CCTV feeds and live terminal monitoring.", "MONITORING")}
                    className="p-2.5 bg-purple-950/80 hover:bg-purple-900 border border-purple-700 text-purple-200 rounded text-xs font-bold transition-colors cursor-pointer flex items-center justify-center space-x-1 shadow"
                  >
                    <Bell className="w-3.5 h-3.5" />
                    <span>MONITOR ATM</span>
                  </button>

                  {/* 4. MARK UNDER INVESTIGATION */}
                  <button
                    onClick={() => handleAction("Marked Under Investigation", "Case allocated to Cyber Command special task force for deep forensic analysis.", "UNDER ANALYSIS")}
                    className="p-2.5 bg-amber-950/80 hover:bg-amber-900 border border-amber-700 text-amber-200 rounded text-xs font-bold transition-colors cursor-pointer flex items-center justify-center space-x-1 shadow"
                  >
                    <RefreshCw className="w-3.5 h-3.5" />
                    <span>MARK UNDER INVESTIGATION</span>
                  </button>

                  {/* 5. GENERATE REPORT */}
                  <button
                    onClick={() => navigate("/reports")}
                    className="p-2.5 bg-emerald-950/80 hover:bg-emerald-900 border border-emerald-700 text-emerald-300 rounded text-xs font-bold transition-colors cursor-pointer flex items-center justify-center space-x-1 shadow"
                  >
                    <FileText className="w-3.5 h-3.5" />
                    <span>GENERATE REPORT</span>
                  </button>

                  {/* 6. UPDATE CASE */}
                  <button
                    onClick={() => setShowUpdateModal(true)}
                    className="p-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-600 text-slate-100 rounded text-xs font-bold transition-colors cursor-pointer flex items-center justify-center space-x-1 shadow"
                  >
                    <Edit3 className="w-3.5 h-3.5" />
                    <span>UPDATE CASE</span>
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

          {/* UPDATE CASE MODAL */}
          {showUpdateModal && (
            <div className="fixed inset-0 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4 z-50">
              <div className="bg-[#0d142b] border-2 border-blue-500/70 rounded-xl p-6 max-w-md w-full shadow-2xl space-y-4">
                <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                  <h3 className="text-sm font-bold text-white flex items-center space-x-2">
                    <Edit3 className="w-4 h-4 text-blue-400" />
                    <span>Update Case File: {detail.case.case_id}</span>
                  </h3>
                  <button
                    onClick={() => setShowUpdateModal(false)}
                    className="text-slate-400 hover:text-white cursor-pointer"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>

                <form onSubmit={handleModalSubmit} className="space-y-4 text-xs">
                  <div>
                    <label className="block text-slate-300 font-semibold mb-1">Update Status To:</label>
                    <select
                      value={modalStatus}
                      onChange={(e) => setModalStatus(e.target.value)}
                      className="w-full bg-slate-900 border border-slate-700 text-white rounded p-2 focus:outline-none focus:border-blue-500 font-mono"
                    >
                      {lifecycle.map((st) => (
                        <option key={st} value={st}>{st}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-slate-300 font-semibold mb-1">Officer Notes / Directive Reason:</label>
                    <textarea
                      rows={3}
                      value={modalNotes}
                      onChange={(e) => setModalNotes(e.target.value)}
                      placeholder="e.g. Received confirmation of ATM CCTV preservation from SBI nodal desk."
                      className="w-full bg-slate-900 border border-slate-700 text-white rounded p-2 focus:outline-none focus:border-blue-500"
                    />
                  </div>

                  <div className="flex justify-end space-x-2 pt-2 border-t border-slate-800">
                    <button
                      type="button"
                      onClick={() => setShowUpdateModal(false)}
                      className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded font-semibold cursor-pointer"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      className="px-4 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded font-bold cursor-pointer"
                    >
                      Save Case Update
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};
