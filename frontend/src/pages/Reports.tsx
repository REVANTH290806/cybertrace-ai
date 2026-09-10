import React, { useEffect, useState } from "react";
import {
  FileText, Printer, Download, ShieldCheck, AlertOctagon,
  IndianRupee, MapPin, Clock, Calendar, CheckCircle
} from "lucide-react";
import { useApp } from "../context/AppContext";
import { api } from "../services/api";

export const Reports: React.FC = () => {
  const { activeCaseId, cases, setActiveCaseId, user } = useApp();
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const loadReport = async (caseId: string) => {
    setLoading(true);
    try {
      const data = await api.getCaseReport(caseId);
      setReport(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeCaseId) {
      loadReport(activeCaseId);
    }
  }, [activeCaseId]);

  const handlePrint = () => {
    window.print();
  };

  const handleDownloadJSON = () => {
    if (!report) return;
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(report, null, 2));
    const downloadAnchor = document.createElement("a");
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `${report.report_id}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div className="p-6 space-y-6">
      {/* Controls Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800 print:hidden">
        <div>
          <h1 className="text-xl font-black text-white flex items-center space-x-2">
            <FileText className="w-5 h-5 text-blue-400" />
            <span>Official Cybercrime Intelligence Report Generator</span>
          </h1>
          <p className="text-xs text-slate-400">
            Court-admissible investigative dossier formatted for judicial and law enforcement compliance
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
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

          <button
            onClick={handleDownloadJSON}
            className="px-3.5 py-2 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs flex items-center space-x-1.5 border border-slate-700 transition-colors cursor-pointer shadow"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download JSON Dossier</span>
          </button>

          <button
            onClick={handlePrint}
            className="px-4 py-2 rounded bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center space-x-1.5 shadow transition-colors cursor-pointer"
          >
            <Printer className="w-4 h-4" />
            <span>Print Official Dossier</span>
          </button>
        </div>
      </div>

      {loading || !report ? (
        <div className="p-12 text-center text-slate-400 text-sm">Compiling official intelligence report...</div>
      ) : (
        /* Formal Government / Law-Enforcement Dossier Sheet */
        <div className="max-w-4xl mx-auto bg-[#0b1022] print:bg-white print:text-black border border-slate-800 print:border-black rounded-lg p-8 shadow-2xl space-y-6">
          {/* Official Letterhead */}
          <div className="text-center pb-4 border-b-2 border-slate-700 print:border-black">
            <div className="text-[11px] font-mono uppercase tracking-widest text-slate-400 print:text-slate-600 font-bold">
              Government of Karnataka // Criminal Investigation Department (CID)
            </div>
            <h2 className="text-lg font-black text-white print:text-black mt-1">
              CYBERCRIME INVESTIGATION DIVISION — SPECIAL OPERATIONAL DOSSIER
            </h2>
            <div className="text-xs font-mono text-red-400 print:text-red-700 font-bold mt-1 tracking-wider">
              {report.classification}
            </div>
          </div>

          {/* Metadata Bar */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-3 bg-slate-900/80 print:bg-slate-100 rounded border border-slate-800 print:border-slate-300 text-xs font-mono">
            <div>
              <span className="text-slate-500 block text-[10px]">REPORT ID</span>
              <span className="font-bold text-white print:text-black">{report.report_id}</span>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px]">DATE & TIME</span>
              <span className="text-slate-300 print:text-black">{report.generated_at}</span>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px]">INVESTIGATING OFFICER</span>
              <span className="font-bold text-blue-400 print:text-black">{user?.full_name}</span>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px]">BADGE ID</span>
              <span className="text-slate-300 print:text-black">{user?.badge_number}</span>
            </div>
          </div>

          {/* Section 1: Case & Complainant Overview */}
          <div className="space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-blue-400 print:text-black border-b border-slate-800 print:border-slate-400 pb-1">
              1. Incident & Complainant Specifics
            </h3>
            <div className="grid grid-cols-2 gap-4 text-xs">
              <div>
                <span className="text-slate-400 print:text-slate-600">Case ID:</span>{" "}
                <span className="font-bold text-white print:text-black font-mono">{report.case_id}</span>
              </div>
              <div>
                <span className="text-slate-400 print:text-slate-600">Fraud Typology:</span>{" "}
                <span className="font-semibold text-white print:text-black">{report.fraud_type}</span>
              </div>
              <div>
                <span className="text-slate-400 print:text-slate-600">Complainant:</span>{" "}
                <span className="font-semibold text-white print:text-black">{report.victim_profile.name}</span>
              </div>
              <div>
                <span className="text-slate-400 print:text-slate-600">Total Defrauded Loss:</span>{" "}
                <span className="font-bold text-red-400 print:text-black font-mono">₹{report.defrauded_amount.toLocaleString()}</span>
              </div>
              <div>
                <span className="text-slate-400 print:text-slate-600">Portal Reference:</span>{" "}
                <span className="font-mono text-slate-300 print:text-black">{report.victim_profile.ncrp_portal_ref}</span>
              </div>
              <div>
                <span className="text-slate-400 print:text-slate-600">Jurisdiction:</span>{" "}
                <span className="text-slate-300 print:text-black">{report.victim_profile.residence}</span>
              </div>
            </div>
          </div>

          {/* Section 2: Predictive Forecasting Intelligence */}
          <div className="space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-blue-400 print:text-black border-b border-slate-800 print:border-slate-400 pb-1">
              2. Predictive AI Liquidation Intelligence
            </h3>
            <div className="p-4 bg-slate-900/60 print:bg-slate-100 rounded border border-slate-800 print:border-slate-300 space-y-2 text-xs">
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono">
                <div>
                  <span className="text-slate-500 block text-[10px]">PREDICTED ATM</span>
                  <span className="font-bold text-white print:text-black">{report.forecasting_summary.predicted_atm}</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px]">TIME WINDOW</span>
                  <span className="font-bold text-amber-400 print:text-black">{report.forecasting_summary.expected_time_window}</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px]">WITHDRAWAL PROBABILITY</span>
                  <span className="font-bold text-red-400 print:text-black">{report.forecasting_summary.withdrawal_probability}</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px]">ESTIMATED CASH-OUT</span>
                  <span className="font-bold text-white print:text-black">₹{report.forecasting_summary.estimated_cash_out.toLocaleString()}</span>
                </div>
              </div>
              <div className="text-[11px] text-slate-400 print:text-slate-700 pt-1">
                Terminal Location: {report.forecasting_summary.location_address}
              </div>
            </div>
          </div>

          {/* Section 3: Transactional Trail Telemetry */}
          <div className="space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-blue-400 print:text-black border-b border-slate-800 print:border-slate-400 pb-1">
              3. Forensic Money Trail Telemetry
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse font-mono">
                <thead>
                  <tr className="border-b border-slate-700 print:border-black text-slate-400 print:text-black text-[10px]">
                    <th className="pb-1">Txn ID</th>
                    <th className="pb-1">Timestamp</th>
                    <th className="pb-1">Source Account</th>
                    <th className="pb-1">Destination Account</th>
                    <th className="pb-1">Amount</th>
                    <th className="pb-1">Channel</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800 print:divide-slate-300 text-slate-300 print:text-black">
                  {report.transaction_trail.map((tx: any) => (
                    <tr key={tx.txn_id}>
                      <td className="py-1.5 font-bold">{tx.txn_id}</td>
                      <td className="py-1.5">{tx.timestamp}</td>
                      <td className="py-1.5">{tx.from_account}</td>
                      <td className="py-1.5">{tx.to_account}</td>
                      <td className="py-1.5 font-bold">₹{tx.amount.toLocaleString()}</td>
                      <td className="py-1.5">{tx.channel}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Section 4: Recommended Statutory Directives */}
          <div className="space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-blue-400 print:text-black border-b border-slate-800 print:border-slate-400 pb-1">
              4. Immediate Statutory Directives
            </h3>
            <ol className="list-decimal list-inside text-xs text-slate-300 print:text-black space-y-1">
              {report.recommended_directives.map((d: string, idx: number) => (
                <li key={idx}>{d}</li>
              ))}
            </ol>
          </div>

          {/* Formal Disclaimer & Signature Block */}
          <div className="pt-6 border-t-2 border-slate-700 print:border-black space-y-6">
            <div className="text-[10px] text-slate-500 print:text-slate-600 italic leading-relaxed text-center">
              {report.disclaimer}
            </div>

            <div className="flex justify-between items-end pt-4 text-xs font-mono">
              <div>
                <div>___________________________________</div>
                <div className="font-bold mt-1">Superintendent of Police</div>
                <div className="text-[10px] text-slate-500 print:text-slate-600">Cyber Crime Command, CID</div>
              </div>
              <div className="text-right">
                <div>___________________________________</div>
                <div className="font-bold mt-1">{user?.full_name}</div>
                <div className="text-[10px] text-slate-500 print:text-slate-600">{user?.role}</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
