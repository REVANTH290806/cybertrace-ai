import os

src_dir = "/Users/revanth/.gemini/antigravity/scratch/cybertrace-ai/frontend/src"
os.makedirs(os.path.join(src_dir, "types"), exist_ok=True)
os.makedirs(os.path.join(src_dir, "services"), exist_ok=True)
os.makedirs(os.path.join(src_dir, "context"), exist_ok=True)
os.makedirs(os.path.join(src_dir, "components"), exist_ok=True)
os.makedirs(os.path.join(src_dir, "pages"), exist_ok=True)

# 1. types/index.ts
with open(os.path.join(src_dir, "types", "index.ts"), "w") as f:
    f.write('''export interface User {
  username: string;
  full_name: string;
  role: string;
  badge_number: string;
}

export interface Case {
  id: number;
  case_id: string;
  fraud_type: string;
  amount: number;
  victim_name: string;
  victim_phone: string;
  victim_location: string;
  status: string;
  risk_level: "HIGH" | "MEDIUM" | "LOW";
  risk_score: number;
  predicted_location_id: string;
  predicted_atm_name: string;
  predicted_time_window: string;
  predicted_amount: number;
  summary: string;
  created_at: string;
  updated_at: string;
}

export interface TimelineAction {
  id: number;
  case_id: string;
  timestamp: string;
  action_type: string;
  description: string;
  officer_id: string;
}

export interface Complaint {
  id: number;
  complaint_id: string;
  case_id: string;
  complainant_name: string;
  incident_date: string;
  portal_ref: string;
  reported_loss: number;
  description: string;
  channel: string;
  created_at: string;
}

export interface CaseDetail {
  case: Case;
  complaint: Complaint | null;
  timeline: TimelineAction[];
}

export interface Transaction {
  id: number;
  transaction_id: string;
  case_id: string;
  timestamp: string;
  source_account: string;
  destination_account: string;
  amount: number;
  transaction_type: string;
  location: string;
  latitude: number | null;
  longitude: number | null;
  device_id: string | null;
  ip_address: string | null;
  channel: string | null;
  beneficiary_bank: string | null;
  risk_indicator: "HIGH" | "MEDIUM" | "LOW";
  layer_depth: number;
  is_suspicious: boolean;
}

export interface GraphNode {
  id: string;
  label: string;
  type: "VICTIM" | "SUSPICIOUS" | "INTERMEDIARY" | "MULE" | "ATM";
  bank: string;
  risk_score: number;
  kyc: string;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  amount: number;
  channel: string;
  timestamp: string;
  risk: string;
  is_predicted?: boolean;
}

export interface TransactionGraphData {
  case_id: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface AccountDetail {
  id: number;
  account_number: string;
  account_holder: string;
  bank_name: string;
  branch: string;
  account_type: string;
  risk_score: number;
  total_incoming: number;
  total_outgoing: number;
  transaction_count: number;
  is_flagged: boolean;
  kyc_status: string;
}

export interface FactorItem {
  name: string;
  contribution: number;
  impact: string;
}

export interface RankedLocationItem {
  rank: number;
  location_id: string;
  name: string;
  probability: number;
  risk: "HIGH" | "MEDIUM" | "LOW";
  distance_km: number;
}

export interface PredictionResult {
  case_id: string;
  predicted_location_id: string;
  predicted_atm_name: string;
  withdrawal_probability: number;
  risk_level: "HIGH" | "MEDIUM" | "LOW";
  predicted_time_window: string;
  predicted_amount: number;
  distance_km: number;
  historical_similarity: number;
  top_factors: FactorItem[];
  ranked_locations: RankedLocationItem[];
}

export interface LocationItem {
  id: number;
  location_id: string;
  name: string;
  bank_name: string;
  address: string;
  latitude: number;
  longitude: number;
  risk_score: number;
  risk_level: "HIGH" | "MEDIUM" | "LOW";
  historical_withdrawals: number;
  average_amount: number;
  last_activity: string;
  area: string;
}

export interface AlertItem {
  id: number;
  alert_id: string;
  case_id: string;
  location_id: string;
  location_name?: string;
  severity: "HIGH" | "MEDIUM" | "LOW";
  probability: number;
  expected_time: string;
  amount: number;
  status: "ACTIVE" | "ACKNOWLEDGED" | "BANK_ALERTED" | "DISPATCHED" | "RESOLVED";
  recommended_action: string;
  created_at: string;
}

export interface IngestionStats {
  records_received: number;
  records_processed: number;
  duplicates_removed: number;
  suspicious_accounts: number;
  suspicious_transactions: number;
  last_ingestion_time: string;
}

export interface AnalyticsSummary {
  total_cases: number;
  total_amount_inr: number;
  high_risk_cases: number;
  medium_risk_cases: number;
  low_risk_cases: number;
  active_alerts: number;
  avg_confidence: number;
}

export interface AnalyticsData {
  summary: AnalyticsSummary;
  risk_distribution: { name: string; value: number; color: string }[];
  fraud_distribution: { type: string; count: number }[];
  hourly_withdrawals: { hour: string; count: number; risk: string }[];
  timeline_trend: { period: string; cases: number; amount: number; prevented: number }[];
  high_risk_locations: { location: string; score: number; withdrawals: number }[];
}
''')

# 2. services/api.ts
with open(os.path.join(src_dir, "services", "api.ts"), "w") as f:
    f.write('''import {
  User, Case, CaseDetail, Transaction, TransactionGraphData,
  AccountDetail, PredictionResult, LocationItem, AlertItem,
  IngestionStats, AnalyticsData
} from "../types";

const API_BASE = "/api";

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`API Error ${res.status}: ${errText || res.statusText}`);
  }
  return res.json();
}

export const api = {
  // Auth
  login: async (username: string, password: string): Promise<User> => {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
    return handleResponse<User>(res);
  },

  // Cases
  getCases: async (params?: { risk?: string; status?: string; fraud_type?: string; q?: string }): Promise<Case[]> => {
    const query = new URLSearchParams();
    if (params?.risk) query.set("risk", params.risk);
    if (params?.status) query.set("status", params.status);
    if (params?.fraud_type) query.set("fraud_type", params.fraud_type);
    if (params?.q) query.set("q", params.q);
    const res = await fetch(`${API_BASE}/cases?${query.toString()}`);
    return handleResponse<Case[]>(res);
  },

  getCaseDetail: async (caseId: string): Promise<CaseDetail> => {
    const res = await fetch(`${API_BASE}/cases/${caseId}`);
    return handleResponse<CaseDetail>(res);
  },

  updateCaseStatus: async (caseId: string, status: string, actionDescription?: string) => {
    const res = await fetch(`${API_BASE}/cases/${caseId}/status`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status, action_description: actionDescription })
    });
    return handleResponse<{ status: string; case: Case }>(res);
  },

  addCaseAction: async (caseId: string, actionType: string, description: string) => {
    const res = await fetch(`${API_BASE}/cases/${caseId}/actions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action_type: actionType, description })
    });
    return handleResponse<{ status: string; action: any }>(res);
  },

  // Transactions
  getTransactions: async (caseId: string): Promise<Transaction[]> => {
    const res = await fetch(`${API_BASE}/transactions/${caseId}`);
    return handleResponse<Transaction[]>(res);
  },

  getTransactionGraph: async (caseId: string): Promise<TransactionGraphData> => {
    const res = await fetch(`${API_BASE}/transactions/${caseId}/graph`);
    return handleResponse<TransactionGraphData>(res);
  },

  getAccountDetail: async (accountNumber: string): Promise<AccountDetail> => {
    const res = await fetch(`${API_BASE}/accounts/${accountNumber}`);
    return handleResponse<AccountDetail>(res);
  },

  // Prediction
  getPrediction: async (caseId: string): Promise<PredictionResult> => {
    const res = await fetch(`${API_BASE}/predict/${caseId}`, { method: "POST" });
    return handleResponse<PredictionResult>(res);
  },

  // Locations
  getLocations: async (): Promise<LocationItem[]> => {
    const res = await fetch(`${API_BASE}/locations`);
    return handleResponse<LocationItem[]>(res);
  },

  getLocationDetail: async (locationId: string) => {
    const res = await fetch(`${API_BASE}/locations/${locationId}`);
    return handleResponse<{ location: LocationItem; nearby_cases: Case[]; active_cases_count: number }>(res);
  },

  // Alerts
  getAlerts: async (status?: string): Promise<AlertItem[]> => {
    const query = status ? `?status=${status}` : "";
    const res = await fetch(`${API_BASE}/alerts${query}`);
    return handleResponse<AlertItem[]>(res);
  },

  createAlert: async (data: {
    case_id: string;
    location_id: string;
    severity?: string;
    probability?: number;
    expected_time?: string;
    amount?: number;
    recommended_action?: string;
  }): Promise<AlertItem> => {
    const res = await fetch(`${API_BASE}/alerts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    return handleResponse<AlertItem>(res);
  },

  updateAlertStatus: async (alertId: string, status: string) => {
    const res = await fetch(`${API_BASE}/alerts/${alertId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status })
    });
    return handleResponse<{ status: string; alert_id: string; new_status: string }>(res);
  },

  simulateAlert: async () => {
    const res = await fetch(`${API_BASE}/alerts/simulate`, { method: "POST" });
    return handleResponse<{ message: string; alert: AlertItem }>(res);
  },

  // Ingestion & Processing
  getIngestionStats: async (): Promise<IngestionStats> => {
    const res = await fetch(`${API_BASE}/ingest/stats`);
    return handleResponse<IngestionStats>(res);
  },

  processData: async () => {
    const res = await fetch(`${API_BASE}/ingest/process`, { method: "POST" });
    return handleResponse<any>(res);
  },

  resetDemoData: async () => {
    const res = await fetch(`${API_BASE}/ingest/reset-demo`, { method: "POST" });
    return handleResponse<any>(res);
  },

  // Analytics
  getAnalytics: async (): Promise<AnalyticsData> => {
    const res = await fetch(`${API_BASE}/analytics`);
    return handleResponse<AnalyticsData>(res);
  },

  // Reports
  getCaseReport: async (caseId: string) => {
    const res = await fetch(`${API_BASE}/reports/${caseId}`, { method: "POST" });
    return handleResponse<any>(res);
  },

  // Health
  getHealth: async () => {
    const res = await fetch(`${API_BASE}/health`);
    return handleResponse<any>(res);
  }
};
''')

# 3. context/AppContext.tsx
with open(os.path.join(src_dir, "context", "AppContext.tsx"), "w") as f:
    f.write('''import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { User, Case, AlertItem } from "../types";
import { api } from "../services/api";

interface AppContextType {
  user: User | null;
  setUser: (u: User | null) => void;
  activeCaseId: string;
  setActiveCaseId: (id: string) => void;
  activeCase: Case | null;
  cases: Case[];
  alerts: AlertItem[];
  unreadAlertsCount: number;
  refreshCases: () => Promise<void>;
  refreshAlerts: () => Promise<void>;
  updateCaseStatus: (newStatus: string, desc?: string) => Promise<void>;
  simulateIncomingAlert: () => Promise<AlertItem | null>;
  isDemoActive: boolean;
  demoStep: number;
  startDemo: () => void;
  nextDemoStep: () => void;
  prevDemoStep: () => void;
  stopDemo: () => void;
  setDemoStep: (step: number) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>({
    username: "demo_officer",
    full_name: "Inspector Vikramaditya Rao",
    role: "Cyber Intelligence Officer",
    badge_number: "CYB-BLR-089"
  });

  const [activeCaseId, setActiveCaseId] = useState<string>("CYB-1024");
  const [cases, setCases] = useState<Case[]>([]);
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [isDemoActive, setIsDemoActive] = useState<boolean>(false);
  const [demoStep, setDemoStep] = useState<number>(1);

  const refreshCases = async () => {
    try {
      const data = await api.getCases();
      setCases(data);
    } catch (err) {
      console.error("Failed to load cases:", err);
    }
  };

  const refreshAlerts = async () => {
    try {
      const data = await api.getAlerts();
      setAlerts(data);
    } catch (err) {
      console.error("Failed to load alerts:", err);
    }
  };

  useEffect(() => {
    refreshCases();
    refreshAlerts();
  }, []);

  const activeCase = cases.find((c) => c.case_id === activeCaseId) || null;
  const unreadAlertsCount = alerts.filter((a) => a.status === "ACTIVE").length;

  const updateCaseStatus = async (newStatus: string, desc?: string) => {
    if (!activeCaseId) return;
    try {
      await api.updateCaseStatus(activeCaseId, newStatus, desc);
      await refreshCases();
    } catch (e) {
      console.error("Failed to update status:", e);
    }
  };

  const simulateIncomingAlert = async (): Promise<AlertItem | null> => {
    try {
      const res = await api.simulateAlert();
      await refreshAlerts();
      return res.alert;
    } catch (e) {
      console.error("Failed to simulate alert:", e);
      return null;
    }
  };

  const startDemo = () => {
    setActiveCaseId("CYB-1024");
    setDemoStep(1);
    setIsDemoActive(true);
  };

  const nextDemoStep = () => {
    setDemoStep((prev) => Math.min(prev + 1, 10));
  };

  const prevDemoStep = () => {
    setDemoStep((prev) => Math.max(prev - 1, 1));
  };

  const stopDemo = () => {
    setIsDemoActive(false);
  };

  return (
    <AppContext.Provider
      value={{
        user,
        setUser,
        activeCaseId,
        setActiveCaseId,
        activeCase,
        cases,
        alerts,
        unreadAlertsCount,
        refreshCases,
        refreshAlerts,
        updateCaseStatus,
        simulateIncomingAlert,
        isDemoActive,
        demoStep,
        startDemo,
        nextDemoStep,
        prevDemoStep,
        stopDemo,
        setDemoStep
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const ctx = useContext(AppContext);
  if (!ctx) {
    throw new Error("useApp must be used within an AppProvider");
  }
  return ctx;
};
''')

print("types, api, and AppContext written successfully.")
