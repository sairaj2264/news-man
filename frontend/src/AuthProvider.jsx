import React, { createContext, useState, useEffect, useContext } from "react";
import { supabase } from "../supabaseClient.js";

// Create a context for authentication
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for an initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setLoading(false);
    });

    // Listen for changes in authentication state (login, logout)
    const { data: authListener } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setSession(session);
        setLoading(false);
      }
    );

    //Just an addition
    // Cleanup the listener when the component unmounts
    //THis is the Auth Provider and some comments are added to increase the readibility
    return () => {
      authListener?.unsubscribe();
    };
  }, []);
//provided Context
  // The value provided to the context consumers
  // Authentication will be Implemented
  const value = {
    session,
    user: session?.user ?? null,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}

// Custom hook to use the auth context
export function useAuth() {
  return useContext(AuthContext);
}
