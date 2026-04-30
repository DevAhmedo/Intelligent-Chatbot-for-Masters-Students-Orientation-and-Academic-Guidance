import { useState } from "react";
import { useAuth } from "./context/AuthContext";
import ChatPage from "./pages/ChatPage";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import LandingPage from "./pages/LandingPage";
import ForgotPasswordPage from "./pages/ForgotPasswordPage";

export default function App() {
  const { isAuthenticated } = useAuth();
  const [view, setView] = useState("landing");

  if (!isAuthenticated) {
    if (view === "login") return <LoginPage onSwitch={() => setView("signup")} onForgot={() => setView("forgot")} />;
    if (view === "signup") return <SignUpPage onSwitch={() => setView("login")} />;
    if (view === "forgot") return <ForgotPasswordPage onBack={() => setView("login")} />;
    return <LandingPage onLogin={() => setView("login")} onSignup={() => setView("signup")} />;
  }

  return <ChatPage />;
}
