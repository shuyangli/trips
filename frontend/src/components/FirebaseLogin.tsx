import { useContext, useEffect } from 'react';
import firebase from 'firebase/compat/app';
import * as firebaseui from 'firebaseui';
import 'firebaseui/dist/firebaseui.css';
import { auth } from '../firebase';
import { AuthStatusContext } from '../contexts/AuthContext';

const FirebaseLogin = () => {
    const { user, loading } = useContext(AuthStatusContext);

    useEffect(() => {
        const ui = firebaseui.auth.AuthUI.getInstance() || new firebaseui.auth.AuthUI(auth);
        const uiConfig = {
            signInSuccessUrl: '/',
            signInOptions: [
                firebase.auth.GoogleAuthProvider.PROVIDER_ID,
            ],
            signInFlow: 'popup',
        };

        // Check if the FirebaseUI widget is already rendered.
        const firebaseUiContainer = document.getElementById('firebaseui-auth-container');
        if (firebaseUiContainer && firebaseUiContainer.childElementCount === 0) {
            ui.start('#firebaseui-auth-container', uiConfig);
        }
    }, [user, loading]);

    if (loading) {
        return <div>Loading...</div>;
    } else if (user !== null) {
        return (
            <div>
                <div>Welcome, {user.displayName || user.email}!</div>
                <button onClick={() => auth.signOut()}>Sign Out</button>
            </div>
        );
    }

    return (
        <div className="google-login-container">
            <div id="firebaseui-auth-container"></div>
            {loading && <div>Loading...</div>}
        </div>
    );
};

export default FirebaseLogin;