export interface User {
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
