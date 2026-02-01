import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const FrequencyGraph = ({ graphData }) => {
    if (!graphData) return null;

    const freqs = graphData.audio1.freqs;
    const psd1 = graphData.audio1.psd;
    const psd2 = graphData.audio2.psd;

    const MAX_FREQ = 8000;

    let processedData = [];
    const stride = 2;

    for (let i = 0; i < freqs.length; i += stride) {
        if (freqs[i] > MAX_FREQ) break;

        processedData.push({
            freq: Math.round(freqs[i]),
            [graphData.audio1.label]: psd1[i],
            [graphData.audio2.label]: psd2[i]
        });
    }

    // Modern color palette
    const color1 = "#8884d8"; // Purple for Audio 1
    const color2 = "#82ca9d"; // Green for Audio 2

    return (
        <div className="glass-pane" style={{ height: '500px', display: 'flex', flexDirection: 'column', padding: '20px' }}>
            <h3 style={{ marginBottom: '20px', fontSize: '1.2rem', fontWeight: '500' }}>Frequency Domain Comparison (PSD)</h3>
            <div style={{ flex: 1, minHeight: 0 }}>
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={processedData} margin={{ top: 10, right: 10, left: 0, bottom: 30 }}>
                        <defs>
                            <linearGradient id="color1" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor={color1} stopOpacity={0.6} />
                                <stop offset="95%" stopColor={color1} stopOpacity={0} />
                            </linearGradient>
                            <linearGradient id="color2" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor={color2} stopOpacity={0.6} />
                                <stop offset="95%" stopColor={color2} stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.05)" />
                        <XAxis
                            dataKey="freq"
                            type="number"
                            domain={[0, MAX_FREQ]}
                            tick={{ fill: '#9ca3af', fontSize: 11 }}
                            tickLine={false}
                            axisLine={false}
                            minTickGap={30}
                            unit=" Hz"
                            label={{ value: 'Frequency (Hz)', position: 'insideBottom', offset: -5, fill: '#9ca3af', fontSize: 12 }}
                        />
                        <YAxis
                            tick={{ fill: '#9ca3af', fontSize: 11 }}
                            tickLine={false}
                            axisLine={false}
                            tickFormatter={(value) => value === 0 ? 0 : value.toExponential(0)}
                            width={65}
                            label={{ value: 'Power Spectral Density', angle: -90, position: 'insideLeft', fill: '#9ca3af', fontSize: 12, style: { textAnchor: 'middle' } }}
                        />
                        <Tooltip
                            contentStyle={{
                                backgroundColor: 'rgba(17, 24, 39, 0.95)',
                                border: '1px solid rgba(255,255,255,0.1)',
                                borderRadius: '8px',
                                color: '#f3f4f6',
                                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                            }}
                            itemStyle={{ padding: 0 }}
                            labelStyle={{ color: '#9ca3af', marginBottom: '5px' }}
                            formatter={(value) => [value.toExponential(2), 'Power']}
                            labelFormatter={(label) => `${label} Hz`}
                        />
                        <Legend
                            verticalAlign="top"
                            height={36}
                            iconType="circle"
                            wrapperStyle={{ paddingBottom: '10px' }}
                        />
                        <Area
                            type="monotone"
                            dataKey={graphData.audio1.label}
                            stroke={color1}
                            fillOpacity={1}
                            fill="url(#color1)"
                            strokeWidth={2}
                            animationDuration={1500}
                        />
                        <Area
                            type="monotone"
                            dataKey={graphData.audio2.label}
                            stroke={color2}
                            fillOpacity={1}
                            fill="url(#color2)"
                            strokeWidth={2}
                            animationDuration={1500}
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default FrequencyGraph;
