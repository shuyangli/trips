import './App.css';

import FirebaseLogin from './components/FirebaseLogin';
import { AuthStatusContext } from './contexts/AuthContext';
import { type AuthStatus, useAuthStatus } from './hooks/useAuthStatus';

function App() {
  const authStatus: AuthStatus = useAuthStatus();
  return (
    <div className="app-container">
      <h1>Welcome to Trips</h1>
      <AuthStatusContext.Provider value={authStatus}>
        <FirebaseLogin />
      </AuthStatusContext.Provider>
    </div>
  );
}

export default App;
