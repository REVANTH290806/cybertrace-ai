import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
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
