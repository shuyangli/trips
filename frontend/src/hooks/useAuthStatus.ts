import { useEffect, useState } from 'react';
import { auth } from '../firebase';
import { onAuthStateChanged, type User } from 'firebase/auth';
import axios from 'axios';

export interface AuthStatus {
    user: User | null;
    idToken: string | null;
    loading: boolean;
}

async function maybeCreateUserInBackend(idToken: string) {
    const response = await axios.post(import.meta.env.VITE_BACKEND_BASE_URL + '/api/v1/auth/update-user', {
        token: idToken,
    });
    return response.data;
}

export const useAuthStatus = () => {
    const [authStatus, setAuthStatus] = useState<AuthStatus>({
        user: null,
        idToken: null,
        loading: true,
    });

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
            if (currentUser) {
                currentUser.getIdToken()
                    .then(token => {
                        maybeCreateUserInBackend(token);
                        setAuthStatus({
                            user: currentUser,
                            idToken: token,
                            loading: false
                        });
                    });
            } else {
                setAuthStatus({
                    user: currentUser,
                    idToken: null,
                    loading: false,
                });
            }
        });

        return () => unsubscribe();
    }, []);
    return authStatus;
};