import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { MapContainer, TileLayer, Marker, Popup, Circle } from "react-leaflet";
import L from "leaflet";
import {
  MapPin, ShieldAlert, AlertTriangle, IndianRupee, Clock,
  ExternalLink, BellRing, Layers, Info, CheckCircle2
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
  const { activeCaseId, activeCase, cases, setActiveCaseId, refreshAlerts } = useApp();
  const [locations, setLocations] = useState<LocationItem[]>([]);
  const [selectedLoc, setSelectedLoc] = useState<LocationItem | null>(null);
  const [toast, setToast] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    api.getLocations().then((locs) => {
      setLocations(locs);
      if (locs.length > 0) setSelectedLoc(locs[0]);
    }).catch(console.error);
  }, []);

  const showToast = (msg: string) => {
    setToast(msg);
    setTimeout(() => setToast(null), 3500);
  };

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
      await refreshAlerts();
      showToast(`Tactical alert dispatched for ${selectedLoc.name}!`);
    } catch (e) {
      console.error(e);
      showToast("Error creating alert");
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

      {toast && (
        <div className="p-3 bg-blue-950/90 border border-blue-500 text-blue-200 rounded text-xs font-semibold flex items-center justify-between shadow-lg">
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>{toast}</span>
          </div>
          <button onClick={() => setToast(null)} className="text-slate-400 hover:text-white cursor-pointer">&times;</button>
        </div>
      )}

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
              const isTarget = Boolean(loc.location_id === "ATM-A102" || (activeCase && loc.location_id === activeCase.predicted_location_id));
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
                      <div className="text-xs p-1 text-slate-900 space-y-1">
                        <div className="font-bold text-sm">{loc.name}</div>
                        <div className="text-slate-600 text-[11px]">{loc.address}</div>
                        <div className="font-bold text-red-600 font-mono">Liquidation Probability: {loc.risk_score}%</div>
                        <div className="pt-1">
                          <button
                            onClick={() => setSelectedLoc(loc)}
                            className="px-2 py-0.5 bg-blue-600 text-white rounded text-[10px] font-bold cursor-pointer"
                          >
                            Inspect Dossier &rarr;
                          </button>
                        </div>
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
                  <div>&bull; Primary Case: <span className="text-blue-400 font-mono font-bold">{activeCaseId}</span></div>
                  <div>&bull; Linked Mule Account: <span className="text-red-400 font-mono">ACC-MULE-204</span></div>
                  <div>&bull; Local Jurisdiction: <span className="text-white">{selectedLoc.area} Police Station</span></div>
                </div>
              </div>

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
                    navigate("/cases");
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
