import React from "react";
import { supabase } from "../supabaseClient";

export default function LogoutButton() {
  const handleLogout = async () => {
    try {
      const { error } = await supabase.auth.signOut();
      if (error) throw error;
      // The onAuthStateChange listener will handle the state update.
    } catch (error) {
      console.error("Error logging out:", error.message);
    }
  };

  return (
    <button
      onClick={handleLogout}
      className="px-4 py-2 font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
    >
      Log Out
    </button>
  );
}
