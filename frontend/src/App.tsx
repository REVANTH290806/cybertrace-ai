import React from "react";
import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";
import { AppProvider, useApp } from "./context/AppContext";
import { Sidebar } from "./components/Sidebar";
import { Header } from "./components/Header";
import { DemoWizard } from "./components/DemoWizard";
import { Login } from "./pages/Login";
import { Dashboard } from "./pages/Dashboard";
import { Cases } from "./pages/Cases";
import { Ingestion } from "./pages/Ingestion";
import { Transactions } from "./pages/Transactions";
import { Predict } from "./pages/Predict";
import { RiskMap } from "./pages/RiskMap";
import { Alerts } from "./pages/Alerts";
import { Analytics } from "./pages/Analytics";
import { Reports } from "./pages/Reports";
import { Settings } from "./pages/Settings";

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useApp();
  const location = useLocation();

  if (!user && location.pathname !== "/login") {
    return <Navigate to="/login" replace />;
  }

  if (location.pathname === "/login") {
    return <>{children}</>;
  }

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#070c1b]">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto custom-scrollbar bg-[#070c1b]">
          {children}
        </main>
      </div>
      <DemoWizard />
    </div>
  );
};

export default function App() {
  return (
    <AppProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/cases" element={<Cases />} />
            <Route path="/ingestion" element={<Ingestion />} />
            <Route path="/transactions" element={<Transactions />} />
            <Route path="/predict" element={<Predict />} />
            <Route path="/map" element={<RiskMap />} />
            <Route path="/alerts" element={<Alerts />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </AppProvider>
  );
}
