import { useContext, useEffect } from "react";
import firebase from "firebase/compat/app";
import * as firebaseui from "firebaseui";
import "firebaseui/dist/firebaseui.css";
import { auth } from "../firebase";
import { AuthStatusContext } from "../contexts/AuthStatusContext";

export const FirebaseLogin = () => {
  const { user, loading } = useContext(AuthStatusContext);

  useEffect(() => {
    const ui =
      firebaseui.auth.AuthUI.getInstance() || new firebaseui.auth.AuthUI(auth);
    const uiConfig: firebaseui.auth.Config = {
      signInOptions: [firebase.auth.GoogleAuthProvider.PROVIDER_ID],
      callbacks: {
        signInSuccessWithAuthResult: () => {
          // Return false to prevent redirect after sign in.
          return false;
        },
      },
      signInFlow: "popup",
    };

    const firebaseUiContainer = document.getElementById(
      "firebaseui-auth-container",
    );
    if (firebaseUiContainer && firebaseUiContainer.childElementCount === 0) {
      ui.start("#firebaseui-auth-container", uiConfig);
    }
  }, [user, loading]);

  if (loading) {
    return <div className="w-8 h-8 bg-gray-200 rounded-full animate-pulse" />;
  } else if (user !== null) {
    return (
      <div className="flex items-center space-x-3">
        {user.photoURL ? (
          <img
            src={user.photoURL}
            alt={user.displayName || user.email || "User"}
            className="w-8 h-8 rounded-full object-cover border"
          />
        ) : (
          <div className="w-8 h-8 flex items-center justify-center bg-gray-300 rounded-full text-sm font-semibold text-gray-700">
            {user.displayName?.[0] || user.email?.[0] || "U"}
          </div>
        )}
        <button
          onClick={() => auth.signOut()}
          className="text-gray-500 hover:text-blue-500 text-sm px-2 py-1 rounded transition border border-gray-200 bg-white"
        >
          Sign Out
        </button>
      </div>
    );
  }

  return (
    <div className="google-login-container flex items-center">
      <div id="firebaseui-auth-container" />
      {loading && <div className="w-8 h-8 bg-gray-200 rounded-full animate-pulse" />}
    </div>
  );
};
