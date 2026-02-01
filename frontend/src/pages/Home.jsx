import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import AudioUploader from '../components/AudioUploader';
import { Activity } from 'lucide-react';

const Home = () => {
    const [file1, setFile1] = useState(null);
    const [file2, setFile2] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleAnalyze = async () => {
        if (!file1 || !file2) return;

        setLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file1', file1);
        formData.append('file2', file2);

        try {
            const response = await axios.post('/analyze', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            navigate('/results', { state: { data: response.data } });
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || "An error occurred during analysis.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="home-container fade-in">
            <header style={{ marginBottom: '3rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '15px', marginBottom: '10px' }}>
                    <Activity size={48} color="var(--color-primary-light)" />
                    <h1>Audio Comparator</h1>
                </div>
                <p>Analyze frequency, intensity, and similarity of voice recordings.</p>
            </header>

            <div style={{ display: 'flex', gap: '20px', justifyContent: 'center', flexWrap: 'wrap' }}>
                <AudioUploader
                    label="First Recording"
                    file={file1}
                    setFile={setFile1}
                    disabled={loading}
                />
                <AudioUploader
                    label="Second Recording"
                    file={file2}
                    setFile={setFile2}
                    disabled={loading}
                />
            </div>

            <div style={{ margin: '30px 0' }}>
                <button
                    className="btn"
                    onClick={handleAnalyze}
                    disabled={!file1 || !file2 || loading}
                    style={{ fontSize: '1.2rem', padding: '10px 30px' }}
                >
                    {loading ? 'Analyzing...' : 'Compare Audio'}
                </button>
            </div>

            {error && (
                <div className="glass-pane" style={{ borderColor: '#f44336', color: '#f44336', maxWidth: '600px', margin: '0 auto' }}>
                    Error: {error}
                </div>
            )}
        </div>
    );
};

export default Home;
