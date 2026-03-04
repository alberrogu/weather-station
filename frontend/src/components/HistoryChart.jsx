import React from 'react';
import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const HistoryChart = ({ data, dataKey, color, title, unit, type = "area", xFormatter = "time" }) => {

    const formatXAxis = (str) => {
        if (!str) return '';
        if (xFormatter === 'date') {
            return new Date(str).toLocaleDateString(undefined, { weekday: 'short', day: 'numeric' });
        }
        return new Date(str).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };

    const formatTooltipLabel = (label) => {
        if (!label) return '';
        if (xFormatter === 'date') {
            return new Date(label).toLocaleDateString();
        }
        return new Date(label).toLocaleString();
    };

    const ChartComponent = type === 'bar' ? BarChart : AreaChart;

    return (
        <div className="glass-panel chart-container">
            <h3 style={{ marginBottom: '1rem', color: 'var(--text-secondary)' }}>{title}</h3>
            <div style={{ width: '100%', height: 300 }}>
                <ResponsiveContainer>
                    <ChartComponent data={data}>
                        <defs>
                            <linearGradient id={`gradient${dataKey}`} x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor={color} stopOpacity={0.3} />
                                <stop offset="95%" stopColor={color} stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="var(--card-border)" vertical={false} />
                        <XAxis
                            dataKey="timestamp"
                            tickFormatter={formatXAxis}
                            stroke="var(--text-secondary)"
                            tick={{ fontSize: 12 }}
                        />
                        <YAxis
                            stroke="var(--text-secondary)"
                            tick={{ fontSize: 12 }}
                            unit={unit}
                        />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#1e293b', border: '1px solid var(--card-border)', borderRadius: '8px' }}
                            itemStyle={{ color: 'var(--text-primary)' }}
                            labelFormatter={formatTooltipLabel}
                        />
                        {type === 'bar' ? (
                            <Bar
                                dataKey={dataKey}
                                fill={color}
                                radius={[4, 4, 0, 0]}
                            />
                        ) : (
                            <Area
                                type="monotone"
                                dataKey={dataKey}
                                stroke={color}
                                fillOpacity={1}
                                fill={`url(#gradient${dataKey})`}
                            />
                        )}
                    </ChartComponent>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default HistoryChart;
