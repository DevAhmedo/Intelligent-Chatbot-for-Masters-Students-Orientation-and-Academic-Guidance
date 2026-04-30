import { createContext, useContext, useState, useCallback } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try {
      const remembered = localStorage.getItem("auth_remember") === "true";
      const stored = remembered
        ? localStorage.getItem("auth_user")
        : sessionStorage.getItem("auth_user");
      // clear any stale localStorage tokens that weren't "keep me signed in"
      if (!remembered) {
        localStorage.removeItem("auth_token");
        localStorage.removeItem("auth_user");
      }
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  });

  const login = useCallback((token, userData, remember = false) => {
    const storage = remember ? localStorage : sessionStorage;
    storage.setItem("auth_token", token);
    storage.setItem("auth_user", JSON.stringify(userData));
    if (remember) {
      localStorage.setItem("auth_remember", "true");
    } else {
      localStorage.removeItem("auth_remember");
    }
    setUser(userData);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("auth_token");
    localStorage.removeItem("auth_user");
    localStorage.removeItem("auth_remember");
    sessionStorage.removeItem("auth_token");
    sessionStorage.removeItem("auth_user");
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}

export function getToken() {
  const remembered = localStorage.getItem("auth_remember") === "true";
  return remembered
    ? localStorage.getItem("auth_token")
    : sessionStorage.getItem("auth_token");
}
