import "./App.css";
import { CreateTrip } from "./components/CreateTrip";
import { TopNav } from "./components/TopNav";
import { AuthStatusContext } from "./contexts/AuthStatusContext";
import { type AuthStatus, useAuthStatus } from "./hooks/useAuthStatus";
import { ConfigProvider } from "antd";

export const App = () => {
  const authStatus: AuthStatus = useAuthStatus();
  return (
    // TODO: figure out the correct locale to use for antd components..
    <ConfigProvider locale={{ locale: navigator.language }}>
      <AuthStatusContext.Provider value={authStatus}>
          <div className="app-container flex flex-col h-screen w-screen justify-between items-center">
            <TopNav />
            <CreateTrip />
          </div>
      </AuthStatusContext.Provider>
    </ConfigProvider>
  );
};
