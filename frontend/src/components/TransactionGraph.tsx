import React, { useState } from "react";
import { Shield, ArrowRight, UserCheck, AlertTriangle, Landmark, MapPin } from "lucide-react";
import { TransactionGraphData, GraphNode } from "../types";

interface TransactionGraphProps {
  data: TransactionGraphData;
  onSelectNode?: (node: GraphNode) => void;
}

export const TransactionGraph: React.FC<TransactionGraphProps> = ({ data, onSelectNode }) => {
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(data.nodes[0] || null);

  const handleNodeClick = (node: GraphNode) => {
    setSelectedNode(node);
    if (onSelectNode) onSelectNode(node);
  };

  const getNodeColor = (type: string) => {
    switch (type) {
      case "VICTIM":
        return { bg: "bg-blue-950/90", border: "border-blue-500", text: "text-blue-400", badge: "VICTIM" };
      case "INTERMEDIARY":
      case "SUSPICIOUS":
        return { bg: "bg-amber-950/90", border: "border-amber-500", text: "text-amber-400", badge: "LAYER" };
      case "MULE":
        return { bg: "bg-red-950/90", border: "border-red-500", text: "text-red-400", badge: "MULE ACCOUNT" };
      case "ATM":
        return { bg: "bg-rose-950/90", border: "border-rose-400", text: "text-rose-300", badge: "TARGET ATM" };
      default:
        return { bg: "bg-slate-900", border: "border-slate-600", text: "text-slate-300", badge: "NODE" };
    }
  };

  return (
    <div className="flex flex-col h-full bg-[#0b1226] border border-slate-800 rounded-lg p-4">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <h3 className="text-sm font-bold text-white">Interactive Money Trail Network</h3>
          <p className="text-xs text-slate-400">Fund dissipation sequence from source victim to forecast cash-out point</p>
        </div>
        <div className="flex items-center space-x-3 text-xs">
          <span className="flex items-center space-x-1.5"><span className="w-2.5 h-2.5 rounded-full bg-blue-500"></span><span className="text-slate-300">Victim</span></span>
          <span className="flex items-center space-x-1.5"><span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span><span className="text-slate-300">Layering Hops</span></span>
          <span className="flex items-center space-x-1.5"><span className="w-2.5 h-2.5 rounded-full bg-red-500"></span><span className="text-slate-300">Mule Node</span></span>
          <span className="flex items-center space-x-1.5"><span className="w-2.5 h-2.5 rounded-full bg-rose-400"></span><span className="text-slate-300">Target ATM</span></span>
        </div>
      </div>

      {/* Flow Sequence Cards */}
      <div className="py-6 overflow-x-auto custom-scrollbar flex items-center space-x-3 min-h-[160px]">
        {data.nodes.map((node, idx) => {
          const style = getNodeColor(node.type);
          const isSelected = selectedNode?.id === node.id;
          const edge = data.edges[idx];

          return (
            <React.Fragment key={node.id}>
              {/* Node Card */}
              <div
                onClick={() => handleNodeClick(node)}
                className={`w-52 shrink-0 p-3.5 rounded-lg border-2 cursor-pointer transition-all ${style.bg} ${
                  isSelected ? `${style.border} ring-2 ring-blue-400/50 scale-105 shadow-xl` : "border-slate-800 hover:border-slate-600"
                }`}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded ${style.bg} ${style.text} border ${style.border}`}>
                    {style.badge}
                  </span>
                  <span className="text-[11px] font-mono text-slate-400">
                    Risk: <span className={node.risk_score > 75 ? "text-red-400 font-bold" : "text-amber-400 font-bold"}>{node.risk_score}%</span>
                  </span>
                </div>
                <div className="text-xs font-bold text-white truncate">{node.label}</div>
                <div className="text-[11px] font-mono text-slate-400 truncate mt-0.5">{node.id}</div>
                <div className="text-[10px] text-slate-400 mt-2 flex items-center justify-between pt-1 border-t border-slate-800/80">
                  <span className="truncate">{node.bank}</span>
                  <span className="font-mono text-slate-500">{node.kyc}</span>
                </div>
              </div>

              {/* Edge arrow with amount and channel */}
              {edge && idx < data.nodes.length - 1 && (
                <div className="flex flex-col items-center justify-center shrink-0 px-1">
                  <span className={`text-[10px] font-bold font-mono px-2 py-0.5 rounded ${edge.is_predicted ? "bg-rose-950 text-rose-300 border border-rose-800" : "bg-slate-900 text-slate-200 border border-slate-700"}`}>
                    ₹{edge.amount.toLocaleString()}
                  </span>
                  <div className="flex items-center text-slate-500 my-1">
                    <div className={`w-8 h-[2px] ${edge.is_predicted ? "bg-rose-500 border-dashed" : "bg-blue-500"}`} />
                    <ArrowRight className={`w-4 h-4 -ml-1 ${edge.is_predicted ? "text-rose-400 animate-pulse" : "text-blue-400"}`} />
                  </div>
                  <span className="text-[9px] font-mono text-slate-400">
                    {edge.channel} ({edge.timestamp})
                  </span>
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* Selected Node Details Drawer */}
      {selectedNode && (
        <div className="mt-auto bg-slate-900/90 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <span className="text-xs font-bold text-white">{selectedNode.label}</span>
              <span className="text-xs font-mono text-slate-400">({selectedNode.id})</span>
              <span className={`text-[10px] px-2 py-0.5 rounded font-semibold ${getNodeColor(selectedNode.type).text} bg-slate-800 border border-slate-700`}>
                {selectedNode.type}
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Institution: <span className="text-slate-200 font-medium">{selectedNode.bank}</span> &bull; KYC Status: <span className="text-slate-200 font-medium">{selectedNode.kyc}</span>
            </p>
          </div>

          <div className="flex items-center space-x-6 text-xs font-mono">
            <div>
              <span className="text-slate-500 block text-[10px]">RISK CLASSIFICATION</span>
              <span className={`font-bold ${selectedNode.risk_score > 70 ? "text-red-400" : "text-amber-400"}`}>
                {selectedNode.risk_score}% ({selectedNode.risk_score > 70 ? "HIGH RISK" : "MODERATE"})
              </span>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px]">INTELLIGENCE DIRECTIVE</span>
              <span className="text-slate-300">
                {selectedNode.type === "MULE" ? "Issue Sec 102 CrPC Freeze" : selectedNode.type === "ATM" ? "Deploy Perimeter Patrol" : "Subpoena Statement"}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
