"use client";
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link'; // To link back to the login page

export default function RegisterPage() {
    const API_URL = process.env.NEXT_PUBLIC_API_URL;

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const router = useRouter();

    const handleRegister = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        if (!username || !password) {
            setError('Username and password are required.');
            return;
        }

        try {
            const response = await fetch(`${API_URL}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                setSuccess(data.message + ' You will be redirected to login shortly.');
                // Redirect to login page after a short delay
                setTimeout(() => {
                    router.push('/login');
                }, 2000);
            } else {
                setError(data.error || 'Registration failed. Please try again.');
            }
        } catch (err) {
            setError('Failed to connect to the server. Please try again later.');
        }
    };

    // Reusing the same simple styles from the login page
    const styles = {
        container: { display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '80vh' },
        form: { display: 'flex', flexDirection: 'column', gap: '1rem', width: '300px', padding: '2rem', border: '1px solid #ccc', borderRadius: '8px' },
        input: { padding: '0.5rem', borderRadius: '4px', border: '1px solid #ccc' },
        button: { padding: '0.75rem', border: 'none', borderRadius: '4px', backgroundColor: '#0070f3', color: 'white', cursor: 'pointer' },
        message: { marginTop: '1rem', textAlign: 'center' },
        error: { color: 'red' },
        success: { color: 'green' },
        link: { marginTop: '1rem', color: '#0070f3', textDecoration: 'underline' }
    };

    return (
        <div style={styles.container}>
            <form onSubmit={handleRegister} style={styles.form}>
                <h2>Register</h2>
                <input
                    type="text"
                    placeholder="Choose a username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    style={styles.input}
                    disabled={!!success} // Disable input on success
                />
                <input
                    type="password"
                    placeholder="Choose a password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={styles.input}
                    disabled={!!success} // Disable input on success
                />
                <button type="submit" style={styles.button} disabled={!!success}>
                    {success ? 'Registered!' : 'Register'}
                </button>
                
                {error && <p style={{...styles.message, ...styles.error}}>{error}</p>}
                {success && <p style={{...styles.message, ...styles.success}}>{success}</p>}
            </form>
            <Link href="/login" style={styles.link}>
                Already have an account? Login here.
            </Link>
        </div>
    );
}