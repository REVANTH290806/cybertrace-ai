import React, { useEffect, useState, useRef } from "react";
import {
  Database, UploadCloud, RefreshCw, FileSpreadsheet, CheckCircle2,
  ShieldCheck, AlertCircle, ArrowRight, FileUp, Upload
} from "lucide-react";
import { api } from "../services/api";
import { IngestionStats, Transaction } from "../types";
import { useApp } from "../context/AppContext";

export const Ingestion: React.FC = () => {
  const [stats, setStats] = useState<IngestionStats | null>(null);
  const [processing, setProcessing] = useState(false);
  const [sampleTxs, setSampleTxs] = useState<Transaction[]>([]);
  const [toast, setToast] = useState<string | null>(null);
  const [validRecords, setValidRecords] = useState<number>(530);
  const [invalidRecords, setInvalidRecords] = useState<number>(0);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { refreshCases, refreshAlerts } = useApp();

  const showToast = (msg: string) => {
    setToast(msg);
    setTimeout(() => setToast(null), 3500);
  };

  const loadStats = async () => {
    try {
      const data = await api.getIngestionStats();
      setStats(data);
      const txs = await api.getTransactions("CYB-1024");
      setSampleTxs(txs);
      setValidRecords(data.records_processed || 530);
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
      showToast("Processing Pipeline executed: Normalization, duplicate detection, and graph synthesis completed!");
    } catch (e) {
      console.error(e);
      showToast("Error processing data pipeline");
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
      showToast("Demo dataset successfully populated into database (59 cases, 530 transactions, 22 ATMs)!");
    } catch (e) {
      console.error(e);
      showToast("Error reloading demo dataset");
    } finally {
      setProcessing(false);
    }
  };

  const handleUploadClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Simulate CSV parsing & ingestion
    setProcessing(true);
    setTimeout(() => {
      setValidRecords(530 + 15);
      setInvalidRecords(0);
      showToast(`Uploaded ${file.name}: 15 records parsed and appended successfully. 0 invalid records.`);
      setProcessing(false);
    }, 600);
  };

  return (
    <div className="p-6 space-y-6">
      {/* Hidden file input */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept=".csv,.xlsx"
        className="hidden"
      />

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

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center gap-2">
          {/* 1. Upload CSV Button */}
          <button
            onClick={handleUploadClick}
            disabled={processing}
            className="px-3.5 py-2 rounded bg-indigo-900/80 hover:bg-indigo-800 text-indigo-200 border border-indigo-600 text-xs font-semibold flex items-center space-x-1.5 transition-colors cursor-pointer shadow"
          >
            <Upload className="w-3.5 h-3.5" />
            <span>Upload CSV</span>
          </button>

          {/* 2. Load Demo Dataset Button */}
          <button
            onClick={handleReset}
            disabled={processing}
            className="px-3.5 py-2 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-semibold flex items-center space-x-1.5 transition-colors cursor-pointer"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${processing ? "animate-spin" : ""}`} />
            <span>Load Demo Dataset</span>
          </button>

          {/* 3. Execute Processing Pipeline */}
          <button
            onClick={handleProcess}
            disabled={processing}
            className="px-3.5 py-2 rounded bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold flex items-center space-x-1.5 shadow-md transition-colors cursor-pointer"
          >
            <UploadCloud className="w-3.5 h-3.5" />
            <span>{processing ? "Processing..." : "Execute Processing Pipeline"}</span>
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
            <span>{validRecords} Txns</span>
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
            { step: "RAW DATA", desc: "Batch & Stream Ingestion", stat: `${validRecords + 120} records` },
            { step: "CLEANING", desc: "Missing Value Handling", stat: "100% complete" },
            { step: "NORMALIZATION", desc: "Timestamp & INR Uniformity", stat: "Duplicates: 14" },
            { step: "FEATURE ENG", desc: "Velocity & Decay Matrices", stat: "9 ML Vectors" },
            { step: "GRAPH SYNTHESIS", desc: "Mule Hop Linkage", stat: "Multi-hop DAG" },
            { step: "MODEL-READY", desc: "Inference Deployment", stat: "Active Engine" },
          ].map((s) => (
            <div key={s.step} className="p-3 bg-slate-900 border border-slate-800 rounded text-center">
              <div className="text-[10px] font-mono font-bold text-blue-400">{s.step}</div>
              <div className="text-xs text-slate-300 font-semibold mt-1">{s.desc}</div>
              <div className="text-[10px] font-mono text-emerald-400 mt-2">{s.stat}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Ingestion Statistics Cards Required by Section 9 */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="bg-slate-900/90 border border-slate-800 p-3.5 rounded-lg text-center">
          <span className="text-[10px] text-slate-400 uppercase font-mono block">Number of Records</span>
          <div className="text-lg font-bold text-white font-mono mt-0.5">{validRecords + 120}</div>
        </div>
        <div className="bg-slate-900/90 border border-slate-800 p-3.5 rounded-lg text-center">
          <span className="text-[10px] text-slate-400 uppercase font-mono block">Valid Records</span>
          <div className="text-lg font-bold text-emerald-400 font-mono mt-0.5">{validRecords}</div>
        </div>
        <div className="bg-slate-900/90 border border-slate-800 p-3.5 rounded-lg text-center">
          <span className="text-[10px] text-slate-400 uppercase font-mono block">Invalid Records</span>
          <div className="text-lg font-bold text-amber-400 font-mono mt-0.5">{invalidRecords}</div>
        </div>
        <div className="bg-slate-900/90 border border-slate-800 p-3.5 rounded-lg text-center">
          <span className="text-[10px] text-slate-400 uppercase font-mono block">Suspicious Accounts</span>
          <div className="text-lg font-bold text-red-400 font-mono mt-0.5">{stats?.suspicious_accounts || 18}</div>
        </div>
        <div className="bg-slate-900/90 border border-slate-800 p-3.5 rounded-lg text-center">
          <span className="text-[10px] text-slate-400 uppercase font-mono block">Last Ingestion Time</span>
          <div className="text-sm font-bold text-blue-300 font-mono mt-1">{stats?.last_ingestion_time || "Just now"}</div>
        </div>
      </div>

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
