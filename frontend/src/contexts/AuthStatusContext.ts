import { createContext } from "react";
import { type AuthStatus } from "../hooks/useAuthStatus";

export const AuthStatusContext = createContext<AuthStatus>({
  user: null,
  loading: false,
});
