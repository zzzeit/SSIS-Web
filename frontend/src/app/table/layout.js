"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function ProtectedLayout({ children }) {
    const router = useRouter();
    const [isAuthenticated, setIsAuthenticated] = useState(false);


    useEffect(() => {
        // Check for the access token in localStorage
        const token = localStorage.getItem('accessToken');

        if (!token) {
            // If no token is found, redirect to the login page
            router.push('/login');
        } else {
            // If a token is found, allow the user to see the page
            // For higher security, you would verify this token with your backend here
            setIsAuthenticated(true);
        }
    }, [router]); // The effect runs once when the component mounts

    // While the check is running, you can show a loading message
    // This prevents a "flash" of the protected content before the redirect happens
    if (!isAuthenticated) {
        return <div>Loading and verifying authentication...</div>; // Or a proper loading spinner
    }

    // If the user is authenticated, render the actual page content
    return <>{children}</>;
}