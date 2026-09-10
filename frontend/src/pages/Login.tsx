import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ShieldAlert, Lock, User, CheckCircle2, ArrowRight } from "lucide-react";
import { useApp } from "../context/AppContext";
import { api } from "../services/api";

export const Login: React.FC = () => {
  const [username, setUsername] = useState("demo_officer");
  const [password, setPassword] = useState("CyberTrace@123");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { setUser } = useApp();
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const user = await api.login(username, password);
      setUser(user);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.message || "Invalid Officer ID or Password");
    } finally {
      setLoading(false);
    }
  };

  const autofillDemo = () => {
    setUsername("demo_officer");
    setPassword("CyberTrace@123");
  };

  return (
    <div className="min-h-screen bg-[#070c1b] flex flex-col items-center justify-center p-4">
      {/* Disclaimer Top */}
      <div className="max-w-md w-full mb-6 p-3 bg-slate-900/90 border border-slate-800 rounded-lg text-center text-xs text-slate-400">
        <span className="font-semibold text-amber-400">PROTOTYPE DEMONSTRATION:</span> Synthetic data only. Intended for SIH26184 evaluation.
      </div>

      <div className="max-w-md w-full bg-[#0d142b] border border-slate-800/90 rounded-xl shadow-2xl p-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex p-3 bg-blue-600/20 border border-blue-500/40 rounded-xl text-blue-400 mb-3">
            <ShieldAlert className="w-8 h-8" />
          </div>
          <h1 className="text-2xl font-black tracking-wider text-white">CYBERTRACE AI</h1>
          <p className="text-xs text-slate-400 mt-1 uppercase tracking-widest font-mono">
            Predictive Cybercrime & Cash Withdrawal Intelligence Platform
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-950/80 border border-red-800 rounded text-xs text-red-300 font-medium">
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Officer ID
            </label>
            <div className="relative">
              <User className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="w-full pl-9 pr-3 py-2.5 bg-slate-900/90 border border-slate-700 rounded text-sm text-white focus:outline-none focus:border-blue-500 font-mono"
                placeholder="Officer ID"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Password
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full pl-9 pr-3 py-2.5 bg-slate-900/90 border border-slate-700 rounded text-sm text-white focus:outline-none focus:border-blue-500 font-mono"
                placeholder="Password"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-500 text-white font-semibold text-sm rounded shadow-lg transition-colors flex items-center justify-center space-x-2 cursor-pointer disabled:opacity-50"
          >
            <span>{loading ? "Authenticating..." : "Access Intelligence Console"}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        {/* Demo Credentials Helper */}
        <div className="mt-6 pt-5 border-t border-slate-800 text-center">
          <div className="text-[11px] text-slate-400 mb-2 font-mono">
            Demo Credentials: <span className="text-white font-bold">demo_officer</span> / <span className="text-white font-bold">CyberTrace@123</span>
          </div>
          <button
            type="button"
            onClick={autofillDemo}
            className="text-xs text-blue-400 hover:text-blue-300 underline font-medium cursor-pointer"
          >
            Auto-fill Demo Credentials
          </button>
        </div>
      </div>
    </div>
  );
};
