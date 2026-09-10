import {
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
