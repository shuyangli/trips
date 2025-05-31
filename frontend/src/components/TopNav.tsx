import { NavLink } from "react-router";
import { FirebaseLogin } from "./FirebaseLogin";

export const TopNav = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-10 w-full bg-white shadow flex items-center justify-between px-8 py-3"> {/* */}
      <div>
        <NavLink
          to="/"
          className={({ isActive }) =>
            `text-xl font-bold tracking-tight mr-4 ${isActive ? "text-blue-600" : "text-gray-700"}`
          }
        >
          Trips
        </NavLink>
      </div>
      <FirebaseLogin /> {/* */}
    </nav>
  );
};
