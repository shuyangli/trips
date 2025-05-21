import { useEffect, useState } from 'react';
import { auth } from '../firebase';
import { onAuthStateChanged, type User } from 'firebase/auth';

export interface AuthStatus {
    user: User | null;
    loading: boolean;
}

export const useAuthStatus = () => {
    const [authStatus, setAuthStatus] = useState<AuthStatus>({
        user: null,
        loading: true,
    });

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
            setAuthStatus({
                user: currentUser,
                loading: false,
            });
            if (currentUser) {
                console.log("User is signed in:", currentUser);
                // You can get the ID token here if needed for your backend
                currentUser.getIdToken()
                    .then(token => {
                        console.log("Firebase ID Token:", token);
                        // TODO: Send this token to your backend for verification if necessary
                    });
            } else {
                console.log("User is signed out");
            }
        });

        // Cleanup subscription on unmount
        return () => unsubscribe();
    }, []);
    return authStatus;
};