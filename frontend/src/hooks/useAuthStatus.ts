import { useEffect, useState } from "react";
import { auth } from "../firebase";
import { onAuthStateChanged, type User } from "firebase/auth";
import { axiosInstance } from "../api/axiosInstance";

export interface AuthStatus {
  user: User | null;
  loading: boolean;
}

async function maybeCreateUserInBackend() {
  try {
    await axiosInstance.post("/signin");
  } catch (error) {
    console.error("Failed to create user in backend:", error);
  }
}

export const useAuthStatus = () => {
  const [authStatus, setAuthStatus] = useState<AuthStatus>({
    user: null,
    loading: true,
  });

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      if (currentUser) {
        maybeCreateUserInBackend();
        setAuthStatus({
          user: currentUser,
          loading: false,
        });
      } else {
        setAuthStatus({
          user: currentUser,
          loading: false,
        });
      }
    });

    return () => unsubscribe();
  }, []);
  return authStatus;
};
