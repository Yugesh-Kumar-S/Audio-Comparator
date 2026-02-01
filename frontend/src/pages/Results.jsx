import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import AnalysisResults from '../components/AnalysisResults';
import FrequencyGraph from '../components/FrequencyGraph';
import { ArrowLeft } from 'lucide-react';

const Results = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const results = location.state?.data;

    useEffect(() => {
        if (!results) {
            navigate('/');
        }
    }, [results, navigate]);

    if (!results) return null;

    return (
        <div className="results-container fade-in" style={{ width: '100%', maxWidth: '1400px', margin: '0 auto' }}>
            <div style={{ display: 'flex', justifyContent: 'flex-start', marginBottom: '20px' }}>
                <button className="btn" onClick={() => navigate('/')} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <ArrowLeft size={20} /> Back to Compare
                </button>
            </div>

            <h1 style={{ marginBottom: '30px' }}>Analysis Results</h1>

            <div className="results-grid">
                <div className="results-left">
                    <AnalysisResults
                        results={{
                            similarity_score: results.similarity_score,
                            breakdown: results.breakdown
                        }}
                        interpretation={results.interpretation}
                    />
                </div>
                <div className="results-right">
                    <FrequencyGraph graphData={results.graph_data} />
                </div>
            </div>
        </div>
    );
};

export default Results;
