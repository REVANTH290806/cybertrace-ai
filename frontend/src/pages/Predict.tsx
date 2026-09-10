import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  BrainCircuit, ShieldAlert, Clock, MapPin, IndianRupee,
  Navigation, CheckCircle2, ChevronRight, BellRing, Eye
} from "lucide-react";
import { useApp } from "../context/AppContext";
import { api } from "../services/api";
import { PredictionResult } from "../types";
import { StatusBadge } from "../components/StatusBadge";

export const Predict: React.FC = () => {
  const { activeCaseId, cases, setActiveCaseId } = useApp();
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const loadPrediction = async (caseId: string) => {
    setLoading(true);
    try {
      const p = await api.getPrediction(caseId);
      setPrediction(p);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeCaseId) {
      loadPrediction(activeCaseId);
    }
  }, [activeCaseId]);

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-xl font-black text-white flex items-center space-x-2">
            <BrainCircuit className="w-5 h-5 text-blue-400" />
            <span>AI Risk Analysis & Predictive Cash Withdrawal Engine</span>
          </h1>
          <p className="text-xs text-slate-400">
            Machine learning forecast of imminent physical ATM cash-out points and temporal windows
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

      {loading || !prediction ? (
        <div className="p-12 text-center text-slate-400 text-sm">Evaluating machine learning risk model...</div>
      ) : (
        <>
          {/* HERO SECTION */}
          <div className="bg-gradient-to-r from-[#170a1e] via-[#101935] to-[#0c142c] border-2 border-red-500/60 rounded-xl p-6 shadow-2xl">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 items-center">
              {/* Main Probability Hero */}
              <div className="md:border-r border-slate-800/80 pr-4 text-center md:text-left">
                <div className="text-[11px] font-mono uppercase font-bold tracking-widest text-slate-400">
                  WITHDRAWAL PROBABILITY
                </div>
                <div className="text-5xl font-black text-white font-mono mt-2 tracking-tight">
                  <span className="text-red-400">{prediction.withdrawal_probability}%</span>
                </div>
                <div className="mt-2 inline-block">
                  <StatusBadge type="risk" value={prediction.risk_level} />
                </div>
              </div>

              {/* Key Predictions */}
              <div className="md:col-span-3 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
                <div className="bg-slate-900/80 border border-slate-800 p-3.5 rounded-lg">
                  <div className="text-slate-400 flex items-center space-x-1 mb-1">
                    <MapPin className="w-3.5 h-3.5 text-blue-400" />
                    <span className="font-semibold uppercase text-[10px]">Predicted Location</span>
                  </div>
                  <div className="text-sm font-bold text-white truncate">{prediction.predicted_atm_name}</div>
                  <div className="text-[10px] text-slate-500 font-mono mt-1">ID: {prediction.predicted_location_id}</div>
                </div>

                <div className="bg-slate-900/80 border border-slate-800 p-3.5 rounded-lg">
                  <div className="text-slate-400 flex items-center space-x-1 mb-1">
                    <Clock className="w-3.5 h-3.5 text-amber-400" />
                    <span className="font-semibold uppercase text-[10px]">Expected Window</span>
                  </div>
                  <div className="text-sm font-bold text-amber-300 font-mono">{prediction.predicted_time_window}</div>
                  <div className="text-[10px] text-slate-500 mt-1">Off-peak liquidity hours</div>
                </div>

                <div className="bg-slate-900/80 border border-slate-800 p-3.5 rounded-lg">
                  <div className="text-slate-400 flex items-center space-x-1 mb-1">
                    <IndianRupee className="w-3.5 h-3.5 text-emerald-400" />
                    <span className="font-semibold uppercase text-[10px]">Predicted Amount</span>
                  </div>
                  <div className="text-sm font-bold text-white font-mono">₹{prediction.predicted_amount.toLocaleString()}</div>
                  <div className="text-[10px] text-slate-500 mt-1">Single / Multiple Tranches</div>
                </div>

                <div className="bg-slate-900/80 border border-slate-800 p-3.5 rounded-lg">
                  <div className="text-slate-400 flex items-center space-x-1 mb-1">
                    <Navigation className="w-3.5 h-3.5 text-purple-400" />
                    <span className="font-semibold uppercase text-[10px]">Spatial Metric</span>
                  </div>
                  <div className="text-sm font-bold text-white font-mono">{prediction.distance_km} km</div>
                  <div className="text-[10px] text-slate-400 mt-1">
                    Similarity: <span className="text-emerald-400 font-bold">{prediction.historical_similarity}%</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-5 pt-4 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs">
              <div className="text-slate-400 flex items-center space-x-2">
                <span className="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
                <span>Immediate law enforcement intervention recommended. Tactical alert ALT-1024 active.</span>
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => navigate("/map")}
                  className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded font-medium flex items-center space-x-1 cursor-pointer"
                >
                  <MapPin className="w-3.5 h-3.5" />
                  <span>Inspect on Bengaluru Map</span>
                </button>
                <button
                  onClick={() => navigate("/alerts")}
                  className="px-3 py-1.5 bg-red-600 hover:bg-red-500 text-white rounded font-medium flex items-center space-x-1 cursor-pointer"
                >
                  <BellRing className="w-3.5 h-3.5" />
                  <span>Dispatched Alerts</span>
                </button>
              </div>
            </div>
          </div>

          {/* EXPLAINABILITY SECTION & RANKED ALTERNATIVES */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Model Explainability Horizontal Bars */}
            <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-5">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-sm font-bold text-white">WHY THIS LOCATION?</h3>
                  <p className="text-xs text-slate-400">Machine learning feature contribution weights</p>
                </div>
                <span className="text-[10px] font-mono text-blue-400 uppercase bg-blue-950 px-2 py-0.5 rounded border border-blue-800">
                  SHAP / Gini Weights
                </span>
              </div>

              <div className="space-y-4">
                {prediction.top_factors.map((f) => (
                  <div key={f.name} className="space-y-1">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-200">{f.name}</span>
                      <span className="font-mono font-bold text-white">{f.contribution}%</span>
                    </div>
                    <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-blue-500 to-indigo-500 h-full rounded-full"
                        style={{ width: `${f.contribution}%` }}
                      />
                    </div>
                    <div className="text-[10px] text-slate-400 italic">{f.impact}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Ranked Alternative Locations */}
            <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-5 flex flex-col">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-sm font-bold text-white">RANKED ALTERNATIVE LOCATIONS</h3>
                  <p className="text-xs text-slate-400">Secondary liquidation nodes identified by clustering</p>
                </div>
                <span className="text-[10px] font-mono text-slate-500">K-Means Spatial Filter</span>
              </div>

              <div className="overflow-x-auto custom-scrollbar flex-1">
                <table className="w-full text-left text-xs border-collapse">
                  <thead>
                    <tr className="border-b border-slate-800 text-slate-400 font-mono text-[11px]">
                      <th className="pb-2.5">Rank</th>
                      <th className="pb-2.5">Terminal</th>
                      <th className="pb-2.5">Probability</th>
                      <th className="pb-2.5">Risk Tier</th>
                      <th className="pb-2.5 text-right">Distance</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 font-medium">
                    {prediction.ranked_locations.map((loc) => (
                      <tr key={loc.location_id} className="hover:bg-slate-800/40">
                        <td className="py-3 font-mono font-bold text-blue-400">#{loc.rank}</td>
                        <td className="py-3 font-bold text-white">
                          <div>{loc.name}</div>
                          <div className="text-[10px] font-mono text-slate-500">{loc.location_id}</div>
                        </td>
                        <td className="py-3 font-mono font-bold text-white">{loc.probability}%</td>
                        <td className="py-3"><StatusBadge type="risk" value={loc.risk} /></td>
                        <td className="py-3 text-right font-mono text-slate-300">{loc.distance_km} km</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400 font-mono">
                Model: RandomForestClassifier (100 estimators, max depth 6) &bull; Calibrated with historical Bengaluru ATM withdrawal velocity patterns.
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
