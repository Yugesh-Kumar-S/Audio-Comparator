import React from 'react';

const AnalysisResults = ({ results, interpretation }) => {
    if (!results) return null;

    const score = results.similarity_score;
    const breakdown = results.breakdown;

    const getScoreColor = (val) => {
        if (val >= 80) return '#4caf50';
        if (val >= 60) return '#ff9800';
        return '#f44336';
    };

    return (
        <div className="glass-pane" style={{ marginTop: '20px', textAlign: 'left' }}>
            <h2 style={{ textAlign: 'center' }}>Similarity Analysis Results</h2>

            <div style={{ textAlign: 'center', marginBottom: '20px' }}>
                <div style={{
                    fontSize: '4rem',
                    fontWeight: 'bold',
                    color: getScoreColor(score),
                    marginBottom: '10px'
                }}>
                    {score.toFixed(1)}%
                </div>
                <p style={{ fontSize: '1.2rem', fontStyle: 'italic' }}>{interpretation}</p>
            </div>

            <h4>Breakdown</h4>
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                gap: '15px'
            }}>
                <ScoreItem label="MFCC Similarity" value={breakdown.mfcc_similarity} />
                <ScoreItem label="Spectral Features" value={breakdown.spectral_similarity} />
                <ScoreItem label="Frequency Distribution" value={breakdown.frequency_distribution_similarity} />
                <ScoreItem label="Temporal Patterns" value={breakdown.temporal_pattern_similarity} />
            </div>
        </div>
    );
};

const ScoreItem = ({ label, value }) => (
    <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        borderBottom: '1px solid rgba(255,255,255,0.1)',
        padding: '5px 0'
    }}>
        <span>{label}</span>
        <span style={{ fontWeight: 'bold' }}>{value.toFixed(1)}%</span>
    </div>
);

export default AnalysisResults;
