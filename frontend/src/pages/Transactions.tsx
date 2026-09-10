import React, { useEffect, useState } from "react";
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
