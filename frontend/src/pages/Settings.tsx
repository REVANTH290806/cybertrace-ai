import React, { useEffect, useState } from "react";
import { Settings as SettingsIcon, ShieldAlert, Cpu, Database, Server, Info, RefreshCw } from "lucide-react";
import { api } from "../services/api";

export const Settings: React.FC = () => {
  const [health, setHealth] = useState<any>(null);
  const [modelSpecs, setModelSpecs] = useState<any>(null);

  useEffect(() => {
    api.getHealth().then(setHealth).catch(console.error);
    fetch("/api/model/features").then(r => r.json()).then(setModelSpecs).catch(console.error);
  }, []);

  return (
    <div className="p-6 space-y-6 max-w-4xl">
      <div className="pb-4 border-b border-slate-800">
        <h1 className="text-xl font-black text-white flex items-center space-x-2">
          <SettingsIcon className="w-5 h-5 text-blue-400" />
          <span>System Information & Configuration</span>
        </h1>
        <p className="text-xs text-slate-400">
          Platform environment, machine learning model parameters, and prototype integrity
        </p>
      </div>

      {/* Legal & Demonstration Disclaimer Card */}
      <div className="bg-amber-950/40 border border-amber-800/80 rounded-lg p-5 space-y-2">
        <div className="flex items-center space-x-2 text-amber-400 font-bold text-xs uppercase tracking-wider">
          <Info className="w-4 h-4" />
          <span>Mandatory Evaluation Disclaimer</span>
        </div>
        <p className="text-xs text-amber-200 leading-relaxed">
          "All prototype predictions use synthetic/anonymized demonstration data and are intended for decision support only. Predictions are decision-support outputs and are not definitive law-enforcement conclusions."
        </p>
      </div>

      {/* Model Specifications */}
      <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-5 space-y-3">
        <h3 className="text-sm font-bold text-white flex items-center space-x-2">
          <Cpu className="w-4 h-4 text-blue-400" />
          <span>Predictive Machine Learning Engine Parameters</span>
        </h3>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-mono">
          <div className="p-3 bg-slate-900 rounded border border-slate-800">
            <span className="text-slate-500 block text-[10px]">MODEL ARCHITECTURE</span>
            <span className="font-bold text-white">{modelSpecs?.model_type || "RandomForestClassifier"}</span>
          </div>
          <div className="p-3 bg-slate-900 rounded border border-slate-800">
            <span className="text-slate-500 block text-[10px]">ESTIMATORS / TREES</span>
            <span className="font-bold text-blue-400">{modelSpecs?.trees || "100 Trees"}</span>
          </div>
          <div className="p-3 bg-slate-900 rounded border border-slate-800">
            <span className="text-slate-500 block text-[10px]">FRAMEWORK</span>
            <span className="font-bold text-purple-400">{modelSpecs?.framework || "scikit-learn"}</span>
          </div>
          <div className="p-3 bg-slate-900 rounded border border-slate-800">
            <span className="text-slate-500 block text-[10px]">STATUS</span>
            <span className="font-bold text-emerald-400">{modelSpecs?.status || "OPERATIONAL"}</span>
          </div>
        </div>

        {modelSpecs?.features && (
          <div className="pt-2">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-2">Engineered Feature Weights</span>
            <div className="space-y-1.5 text-xs">
              {modelSpecs.features.map((f: any) => (
                <div key={f.feature} className="flex items-center justify-between p-2 bg-slate-900/60 rounded border border-slate-800">
                  <div>
                    <span className="font-mono text-slate-200">{f.feature}</span>
                    <span className="text-[10px] text-slate-500 ml-2">({f.description})</span>
                  </div>
                  <span className="font-mono font-bold text-blue-400">{(f.weight * 100).toFixed(0)}% weight</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Infrastructure Details */}
      <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-5 space-y-3">
        <h3 className="text-sm font-bold text-white flex items-center space-x-2">
          <Server className="w-4 h-4 text-emerald-400" />
          <span>Backend & Database Infrastructure</span>
        </h3>

        <div className="space-y-2 text-xs font-mono">
          <div className="flex items-center justify-between p-2 bg-slate-900/60 rounded border border-slate-800">
            <span className="text-slate-400">Application Server</span>
            <span className="text-white">FastAPI 0.141 / Uvicorn (Python 3.13)</span>
          </div>
          <div className="flex items-center justify-between p-2 bg-slate-900/60 rounded border border-slate-800">
            <span className="text-slate-400">Database Layer</span>
            <span className="text-white">SQLite (Structured for PostgreSQL / PostGIS migration)</span>
          </div>
          <div className="flex items-center justify-between p-2 bg-slate-900/60 rounded border border-slate-800">
            <span className="text-slate-400">GIS Mapping Library</span>
            <span className="text-white">Leaflet 1.9 / OpenStreetMap (Bengaluru Metropolitan Region)</span>
          </div>
          <div className="flex items-center justify-between p-2 bg-slate-900/60 rounded border border-slate-800">
            <span className="text-slate-400">Frontend Stack</span>
            <span className="text-white">React 19, TypeScript, Vite, Tailwind CSS v4, Recharts</span>
          </div>
        </div>
      </div>
    </div>
  );
};
