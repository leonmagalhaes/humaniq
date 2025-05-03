"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { auth, users } from "@/lib/api";
import type { User } from "@/lib/types";

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem("token");
        if (token) {
          const userData = await users.getProfile();
          setUser(userData);
        }
      } catch (error) {
        console.error("Auth check failed:", error);
        localStorage.removeItem("token");
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const userData = await auth.login(email, password);
      setUser(userData);
      router.push("/dashboard");
      return userData;
    } catch (error) {
      console.error("Login failed:", error);
      throw error;
    }
  };

  const register = async (name: string, email: string, password: string) => {
    try {
      const userData = await auth.register(name, email, password);
      setUser(userData);
      router.push("/initial-test");
      return userData;
    } catch (error) {
      console.error("Registration failed:", error);
      throw error;
    }
  };

  const logout = () => {
    auth.logout();
    setUser(null);
    router.push("/login");
  };

  return {
    user,
    loading,
    login,
    register,
    logout,
  };
}