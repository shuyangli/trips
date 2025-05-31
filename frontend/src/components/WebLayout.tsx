import { Outlet } from "react-router";
import { TopNav } from "./TopNav";
import "./WebLayout.css";

export const WebLayout = () => {
  return (
    <div className="app-container flex flex-col min-h-screen w-screen items-center bg-gray-100">
      <TopNav />
      <main className="trips-main flex-grow w-full flex justify-center py-8 px-4">
        <Outlet />
      </main>
    </div>
  );
};
