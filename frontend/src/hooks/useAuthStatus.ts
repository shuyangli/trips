import { useEffect, useState } from "react";
import { auth } from "../firebase";
import { onAuthStateChanged, type User } from "firebase/auth";
import { axiosInstance } from "../api/axiosInstance";

export interface AuthStatus {
  user: User | null;
  loading: boolean;
}

function maybeCreateUserInBackend() {
  // Not sure if this is still needed if we're injecting the token on the header.
  axiosInstance.post("/signin");
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
