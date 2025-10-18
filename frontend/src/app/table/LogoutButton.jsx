"use client";

import { useRouter } from 'next/navigation';
import './LogoutButton.css';

export default function LogoutButton() {
    const router = useRouter();

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        router.push('/login'); // Redirects to the login page
    };

    return (
        <button onClick={handleLogout} className='logout-button' >
            Logout
        </button>
    );
}