"use client";
import { useState } from 'react';
import { useRouter } from 'next/navigation'; // For redirection

export default function LoginPage() {
    const API_URL = process.env.NEXT_PUBLIC_API_URL;

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const router = useRouter();

    const handleLogin = async (e) => {
        e.preventDefault(); // Prevent form from reloading the page
        setError('');

        if (!username || !password) {
            setError('Username and password are required.');
            return;
        }

        try {
            const response = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            if (response.ok) {
                const data = await response.json();
                // Store the token and redirect
                localStorage.setItem('accessToken', data.access_token);
                router.push('/table/colleges'); // Redirect to a protected page
            } else {
                const errorData = await response.json();
                setError(errorData.error || 'Login failed.');
            }
        } catch (err) {
            setError('Failed to connect to the server. Please try again later.');
        }
    };

    // Basic inline styles for demonstration
    const styles = {
        container: { display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '80vh' },
        form: { display: 'flex', flexDirection: 'column', gap: '1rem', width: '300px', padding: '2rem', border: '1px solid #ccc', borderRadius: '8px' },
        input: { padding: '0.5rem', borderRadius: '4px', border: '1px solid #ccc' },
        button: { padding: '0.75rem', border: 'none', borderRadius: '4px', backgroundColor: '#0070f3', color: 'white', cursor: 'pointer' },
        error: { color: 'red', marginTop: '1rem' }
    };

    return (
        <div style={styles.container}>
            <form onSubmit={handleLogin} style={styles.form}>
                <h2>Login</h2>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    style={styles.input}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={styles.input}
                />
                <button type="submit" style={styles.button}>Login</button>
                {error && <p style={styles.error}>{error}</p>}
            </form>
        </div>
    );
}