import os

pages_dir = "/Users/revanth/.gemini/antigravity/scratch/cybertrace-ai/frontend/src/pages"

# 6. Predict.tsx
with open(os.path.join(pages_dir, "Predict.tsx"), "w") as f:
    f.write('''import React, { useEffect, useState } from "react";
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
''')

# 7. RiskMap.tsx
with open(os.path.join(pages_dir, "RiskMap.tsx"), "w") as f:
    f.write('''import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, Circle } from "react-leaflet";
import L from "leaflet";
import {
  MapPin, ShieldAlert, AlertTriangle, IndianRupee, Clock,
  ExternalLink, BellRing, Layers, Info
} from "lucide-react";
import { useApp } from "../context/AppContext";
import { api } from "../services/api";
import { LocationItem } from "../types";
import { StatusBadge } from "../components/StatusBadge";

// Custom Leaflet DivIcons with pulsing rings for high risk
const createMarkerIcon = (risk: string, isTarget: boolean) => {
  const color = risk === "HIGH" ? "#ef4444" : risk === "MEDIUM" ? "#f59e0b" : "#10b981";
  const size = isTarget ? 34 : 26;
  const pulse = isTarget ? '<span class="absolute -inset-1 rounded-full bg-red-500 animate-ping opacity-75"></span>' : '';

  return L.divIcon({
    className: "custom-leaflet-marker",
    html: `
      <div class="relative flex items-center justify-center">
        ${pulse}
        <div style="background-color: ${color}; width: ${size}px; height: ${size}px; border: 2px solid white; box-shadow: 0 0 10px rgba(0,0,0,0.5);" class="rounded-full flex items-center justify-center text-white font-bold text-[10px]">
          ${isTarget ? '★' : 'ATM'}
        </div>
      </div>
    `,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
  });
};

export const RiskMap: React.FC = () => {
  const { activeCaseId, activeCase, cases, setActiveCaseId } = useApp();
  const [locations, setLocations] = useState<LocationItem[]>([]);
  const [selectedLoc, setSelectedLoc] = useState<LocationItem | null>(null);
  const [alertSuccess, setAlertSuccess] = useState(false);

  useEffect(() => {
    api.getLocations().then((locs) => {
      setLocations(locs);
      if (locs.length > 0) setSelectedLoc(locs[0]);
    }).catch(console.error);
  }, []);

  const handleCreateAlert = async () => {
    if (!selectedLoc) return;
    try {
      await api.createAlert({
        case_id: activeCaseId,
        location_id: selectedLoc.location_id,
        severity: selectedLoc.risk_level,
        probability: selectedLoc.risk_score,
        expected_time: "23:30 – 00:30",
        amount: activeCase?.amount || 185000,
        recommended_action: `Dispatch perimeter patrol to ${selectedLoc.name}. Real-time withdrawal alert.`
      });
      setAlertSuccess(true);
      setTimeout(() => setAlertSuccess(false), 3000);
    } catch (e) {
      console.error(e);
    }
  };

  // Center on Bengaluru
  const centerPosition: [number, number] = [12.9716, 77.5946];

  return (
    <div className="p-6 space-y-4 h-[calc(100vh-60px)] flex flex-col">
      {/* Header & Map Disclaimer */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 pb-2 border-b border-slate-800 shrink-0">
        <div>
          <h1 className="text-xl font-black text-white flex items-center space-x-2">
            <MapPin className="w-5 h-5 text-blue-400" />
            <span>Predictive Risk Map (Bengaluru Metropolitan Region)</span>
          </h1>
          <p className="text-xs text-amber-400 font-semibold flex items-center space-x-1.5 mt-0.5">
            <Info className="w-3.5 h-3.5" />
            <span>SYNTHETIC DEMONSTRATION DATA &bull; Predictive ATM liquidation heat zones</span>
          </p>
        </div>

        {/* Legend */}
        <div className="flex items-center space-x-4 text-xs font-mono bg-slate-900 px-3 py-1.5 rounded border border-slate-800">
          <span className="flex items-center space-x-1.5"><span className="w-3 h-3 rounded-full bg-red-500"></span><span className="text-slate-300">HIGH RISK (≥70%)</span></span>
          <span className="flex items-center space-x-1.5"><span className="w-3 h-3 rounded-full bg-amber-500"></span><span className="text-slate-300">MEDIUM (40-69%)</span></span>
          <span className="flex items-center space-x-1.5"><span className="w-3 h-3 rounded-full bg-emerald-500"></span><span className="text-slate-300">LOW (&lt;40%)</span></span>
          <span className="flex items-center space-x-1.5"><span className="w-3 h-3 rounded-full bg-red-500 flex items-center justify-center text-[8px] text-white">★</span><span className="text-white font-bold">Target Forecast</span></span>
        </div>
      </div>

      {/* Main Map Body: Left Map (70%), Right Intelligence Panel (30%) */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-4 min-h-0">
        {/* Leaflet Map */}
        <div className="lg:col-span-3 rounded-lg overflow-hidden border border-slate-800 relative z-10">
          <MapContainer
            center={centerPosition}
            zoom={12}
            scrollWheelZoom={true}
            style={{ height: "100%", width: "100%" }}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {/* Render ATM Markers */}
            {locations.map((loc) => {
              const isTarget = loc.location_id === "ATM-A102" || (activeCase && loc.location_id === activeCase.predicted_location_id);
              return (
                <React.Fragment key={loc.location_id}>
                  <Marker
                    position={[loc.latitude, loc.longitude]}
                    icon={createMarkerIcon(loc.risk_level, isTarget)}
                    eventHandlers={{
                      click: () => setSelectedLoc(loc),
                    }}
                  >
                    <Popup>
                      <div className="text-xs p-1">
                        <div className="font-bold text-slate-900">{loc.name}</div>
                        <div className="text-slate-600">{loc.address}</div>
                        <div className="mt-1 font-bold text-red-600">Risk Score: {loc.risk_score}%</div>
                      </div>
                    </Popup>
                  </Marker>

                  {/* High risk radius circle */}
                  {loc.risk_level === "HIGH" && (
                    <Circle
                      center={[loc.latitude, loc.longitude]}
                      radius={isTarget ? 700 : 400}
                      pathOptions={{
                        color: "#ef4444",
                        fillColor: "#ef4444",
                        fillOpacity: 0.15,
                        weight: isTarget ? 2 : 1
                      }}
                    />
                  )}
                </React.Fragment>
              );
            })}
          </MapContainer>
        </div>

        {/* Right Intelligence Panel */}
        <div className="bg-[#0e162f] border border-slate-800 rounded-lg p-5 flex flex-col justify-between overflow-y-auto custom-scrollbar">
          {selectedLoc ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">ATM Intelligence Dossier</span>
                <StatusBadge type="risk" value={selectedLoc.risk_level} />
              </div>

              <div>
                <h3 className="text-base font-bold text-white">{selectedLoc.name}</h3>
                <p className="text-xs text-slate-400 mt-1">{selectedLoc.address}</p>
                <div className="text-[11px] font-mono text-slate-500 mt-0.5">ID: {selectedLoc.location_id} &bull; {selectedLoc.bank_name}</div>
              </div>

              <div className="space-y-2.5 text-xs bg-slate-900/80 p-3.5 rounded border border-slate-800">
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Liquidation Probability</span>
                  <span className="font-mono font-bold text-red-400 text-sm">{selectedLoc.risk_score}%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Predicted Cash-out</span>
                  <span className="font-mono font-bold text-white">₹{selectedLoc.average_amount.toLocaleString()}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Expected Time</span>
                  <span className="font-mono text-amber-300">23:30 – 00:30</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Historical Withdrawals</span>
                  <span className="font-mono text-slate-300">{selectedLoc.historical_withdrawals} incidents</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Terminal Last Active</span>
                  <span className="font-mono text-slate-400">{selectedLoc.last_activity}</span>
                </div>
              </div>

              <div className="space-y-2">
                <span className="text-[11px] font-bold text-slate-300 uppercase tracking-wider block">Connected Cybercrime Syndicates</span>
                <div className="text-xs text-slate-400 bg-slate-900/50 p-2.5 rounded border border-slate-800 space-y-1">
                  <div>&bull; Primary Case: <span className="text-blue-400 font-mono font-bold">CYB-1024</span></div>
                  <div>&bull; Linked Mule Account: <span className="text-red-400 font-mono">ACC-MULE-204</span></div>
                  <div>&bull; Local Jurisdiction: <span className="text-white">{selectedLoc.area} Police Station</span></div>
                </div>
              </div>

              {alertSuccess && (
                <div className="p-2 bg-emerald-950/80 border border-emerald-800 text-emerald-300 rounded text-xs text-center font-semibold">
                  Field Intervention Alert Dispatched!
                </div>
              )}

              <div className="pt-2 space-y-2">
                <button
                  onClick={handleCreateAlert}
                  className="w-full py-2.5 px-3 bg-red-600 hover:bg-red-500 text-white font-bold text-xs rounded transition-colors flex items-center justify-center space-x-2 shadow-lg cursor-pointer"
                >
                  <BellRing className="w-4 h-4" />
                  <span>Create Law-Enforcement Alert</span>
                </button>

                <button
                  onClick={() => {
                    setActiveCaseId("CYB-1024");
                    window.location.href = "/cases";
                  }}
                  className="w-full py-2 px-3 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs rounded font-semibold transition-colors flex items-center justify-center space-x-1 cursor-pointer"
                >
                  <span>View Intelligence Profile</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ) : (
            <div className="text-center text-slate-500 text-xs py-12">Click any ATM marker on the map to inspect intelligence.</div>
          )}
        </div>
      </div>
    </div>
  );
};
''')

# 8. Alerts.tsx
with open(os.path.join(pages_dir, "Alerts.tsx"), "w") as f:
    f.write('''import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Bell, BellRing, AlertOctagon, CheckCircle2, Send, Radio,
  Sparkles, Filter, ShieldCheck, MapPin, IndianRupee
} from "lucide-react";
import { useApp } from "../context/AppContext";
import { api } from "../services/api";
import { AlertItem } from "../types";
import { StatusBadge } from "../components/StatusBadge";

export const Alerts: React.FC = () => {
  const { alerts, refreshAlerts, setActiveCaseId, simulateIncomingAlert } = useApp();
  const [filter, setFilter] = useState<string>("ALL");
  const [simulating, setSimulating] = useState(false);
  const [toast, setToast] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleStatusUpdate = async (alertId: string, newStatus: string) => {
    try {
      await api.updateAlertStatus(alertId, newStatus);
      await refreshAlerts();
      setToast(`Alert ${alertId} updated to ${newStatus}`);
      setTimeout(() => setToast(null), 3000);
    } catch (e) {
      console.error(e);
    }
  };

  const handleSimulate = async () => {
    setSimulating(true);
    const newAlert = await simulateIncomingAlert();
    setSimulating(false);
    if (newAlert) {
      setToast(`Simulated high-risk alert ${newAlert.alert_id} generated!`);
      setTimeout(() => setToast(null), 4000);
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
            className="px-3.5 py-2 rounded bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white text-xs font-bold shadow-lg flex items-center space-x-1.5 transition-all cursor-pointer"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>{simulating ? "Simulating..." : "Simulate Incoming Alert"}</span>
          </button>
        </div>
      </div>

      {toast && (
        <div className="p-3 bg-blue-950/90 border border-blue-600 text-blue-300 rounded text-xs font-semibold flex items-center justify-between">
          <span>{toast}</span>
          <button onClick={() => setToast(null)} className="text-slate-400 hover:text-white">&times;</button>
        </div>
      )}

      {/* Filter Tabs */}
      <div className="flex space-x-2 border-b border-slate-800 pb-2">
        {["ALL", "ACTIVE", "ACKNOWLEDGED", "DISPATCHED"].map((tab) => (
          <button
            key={tab}
            onClick={() => setFilter(tab)}
            className={`px-3 py-1.5 rounded text-xs font-semibold transition-colors cursor-pointer ${
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

              <div className="text-xs text-slate-300 bg-slate-900/50 p-2 rounded border border-slate-800">
                <span className="text-[10px] font-semibold text-slate-500 uppercase block mb-0.5">Recommended Protocol</span>
                {a.recommended_action}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="pt-2 border-t border-slate-800 flex flex-wrap items-center justify-between gap-2">
              <div className="flex items-center space-x-1.5">
                <span className="text-[10px] text-slate-500 font-mono">Status:</span>
                <span className="text-[10px] font-bold font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                  {a.status}
                </span>
              </div>

              <div className="flex items-center space-x-2 text-xs">
                {a.status === "ACTIVE" && (
                  <button
                    onClick={() => handleStatusUpdate(a.alert_id, "ACKNOWLEDGED")}
                    className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded font-semibold cursor-pointer"
                  >
                    Acknowledge
                  </button>
                )}

                <button
                  onClick={() => handleStatusUpdate(a.alert_id, "DISPATCHED")}
                  className="px-2.5 py-1 bg-blue-900 hover:bg-blue-800 text-blue-200 border border-blue-700 rounded font-semibold flex items-center space-x-1 cursor-pointer"
                >
                  <Radio className="w-3 h-3" />
                  <span>Dispatch Team</span>
                </button>

                <button
                  onClick={() => {
                    setActiveCaseId(a.case_id);
                    navigate("/cases");
                  }}
                  className="px-2.5 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded font-semibold cursor-pointer"
                >
                  View Case &rarr;
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
''')

# 9. Analytics.tsx
with open(os.path.join(pages_dir, "Analytics.tsx"), "w") as f:
    f.write('''import React, { useEffect, useState } from "react";
import {
  BarChart3, PieChart, TrendingUp, ShieldAlert, Filter,
  IndianRupee, FolderSearch, AlertTriangle, Clock
} from "lucide-react";
import {
  AreaChart, Area, BarChart, Bar, PieChart as RePieChart, Pie, Cell,
  XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend
} from "recharts";
import { api } from "../services/api";
import { AnalyticsData } from "../types";

export const Analytics: React.FC = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [selectedRisk, setSelectedRisk] = useState<string>("ALL");

  useEffect(() => {
    api.getAnalytics().then(setData).catch(console.error);
  }, []);

  if (!data) {
    return <div className="p-12 text-center text-slate-400 text-sm">Computing analytical metrics...</div>;
  }

  const COLORS = ["#ef4444", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6", "#ec4899"];

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-xl font-black text-white flex items-center space-x-2">
            <BarChart3 className="w-5 h-5 text-blue-400" />
            <span>Cybercrime & Liquidation Analytics Intelligence</span>
          </h1>
          <p className="text-xs text-slate-400">
            Macroscopic trends, temporal liquidation vectors, and hot-zone density
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs">
          <span className="text-slate-400">Risk Filter:</span>
          <select
            value={selectedRisk}
            onChange={(e) => setSelectedRisk(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-white rounded px-2.5 py-1 text-xs"
          >
            <option value="ALL">All Risk Tiers</option>
            <option value="HIGH">High Risk Only</option>
            <option value="MEDIUM">Medium Risk</option>
          </select>
        </div>
      </div>

      {/* Analytical Visual Grid (8 Charts) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* KPI 1 */}
        <div className="bg-[#0e162f] border border-slate-800 p-4 rounded-lg">
          <span className="text-xs text-slate-400 uppercase font-semibold">Total Case Volume</span>
          <div className="text-2xl font-black text-white font-mono mt-1">{data.summary.total_cases}</div>
          <span className="text-[11px] text-blue-400 font-mono">100% telemetry coverage</span>
        </div>
        {/* KPI 2 */}
        <div className="bg-[#0e162f] border border-slate-800 p-4 rounded-lg">
          <span className="text-xs text-slate-400 uppercase font-semibold">Loss Pool Investigated</span>
          <div className="text-2xl font-black text-amber-400 font-mono mt-1">₹3.86 Cr</div>
          <span className="text-[11px] text-slate-400 font-mono">Across 7 fraud typologies</span>
        </div>
        {/* KPI 3 */}
        <div className="bg-[#0e162f] border border-slate-800 p-4 rounded-lg">
          <span className="text-xs text-slate-400 uppercase font-semibold">High-Risk Cashout Threat</span>
          <div className="text-2xl font-black text-red-400 font-mono mt-1">{data.summary.high_risk_cases}</div>
          <span className="text-[11px] text-red-400/80 font-mono">Probability &gt; 70%</span>
        </div>
        {/* KPI 4 */}
        <div className="bg-[#0e162f] border border-slate-800 p-4 rounded-lg">
          <span className="text-xs text-slate-400 uppercase font-semibold">Model Confidence</span>
          <div className="text-2xl font-black text-emerald-400 font-mono mt-1">{data.summary.avg_confidence}%</div>
          <span className="text-[11px] text-emerald-400/80 font-mono">Random Forest 100 Trees</span>
        </div>
      </div>

      {/* Row 1: Weekly Incident Velocity & Fraud Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Weekly Trend */}
        <div className="bg-[#0e162f] border border-slate-800 p-5 rounded-lg">
          <h3 className="text-sm font-bold text-white mb-3">1. Cybercrime Cases & Loss Pool Over Time</h3>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.timeline_trend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="period" stroke="#64748b" fontSize={10} />
                <YAxis stroke="#64748b" fontSize={10} />
                <Tooltip contentStyle={{ backgroundColor: "#090e1f", borderColor: "#334155", fontSize: 11 }} />
                <Area type="monotone" dataKey="amount" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.2} name="Total Loss (₹)" />
                <Area type="monotone" dataKey="prevented" stroke="#10b981" fill="#10b981" fillOpacity={0.3} name="Prevented Loss (₹)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Hourly Withdrawals Profile */}
        <div className="bg-[#0e162f] border border-slate-800 p-5 rounded-lg">
          <h3 className="text-sm font-bold text-white mb-3">2. ATM Cash-Out Frequency by Hour of Day</h3>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.hourly_withdrawals}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="hour" stroke="#64748b" fontSize={10} />
                <YAxis stroke="#64748b" fontSize={10} />
                <Tooltip contentStyle={{ backgroundColor: "#090e1f", borderColor: "#334155", fontSize: 11 }} />
                <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} name="Attempted Withdrawals" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Row 2: Risk Tier Distribution & Top High-Risk Locations */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Risk Distribution Donut */}
        <div className="bg-[#0e162f] border border-slate-800 p-5 rounded-lg">
          <h3 className="text-sm font-bold text-white mb-3">3. Case Risk Classification Breakdown</h3>
          <div className="h-64 w-full flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <RePieChart>
                <Pie
                  data={data.risk_distribution}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={5}
                >
                  {data.risk_distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: "#090e1f", borderColor: "#334155", fontSize: 11 }} />
                <Legend />
              </RePieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* High-Risk ATM Locations Bar */}
        <div className="bg-[#0e162f] border border-slate-800 p-5 rounded-lg">
          <h3 className="text-sm font-bold text-white mb-3">4. Top High-Risk ATM Cash-Out Hotspots</h3>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.high_risk_locations} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis type="number" stroke="#64748b" fontSize={10} />
                <YAxis dataKey="location" type="category" stroke="#64748b" fontSize={10} width={90} />
                <Tooltip contentStyle={{ backgroundColor: "#090e1f", borderColor: "#334155", fontSize: 11 }} />
                <Bar dataKey="score" fill="#ef4444" radius={[0, 4, 4, 0]} name="Risk Index" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
''')

# 10. Reports.tsx
with open(os.path.join(pages_dir, "Reports.tsx"), "w") as f:
    f.write('''import React, { useEffect, useState } from "react";
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

          <button
            onClick={handlePrint}
            className="px-4 py-2 rounded bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center space-x-1.5 shadow transition-colors cursor-pointer"
          >
            <Printer className="w-4 h-4" />
            <span>Generate & Print Report</span>
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
''')

# 11. Settings.tsx
with open(os.path.join(pages_dir, "Settings.tsx"), "w") as f:
    f.write('''import React, { useEffect, useState } from "react";
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
''')

print("Pages 2 (Predict, RiskMap, Alerts, Analytics, Reports, Settings) created successfully.")
