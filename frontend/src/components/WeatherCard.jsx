import React from 'react';

const WeatherCard = ({ title, value, unit, icon: Icon, color = "#38bdf8" }) => {
    return (
        <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: 'var(--text-secondary)' }}>
                <span style={{ fontSize: '0.9rem', fontWeight: 500 }}>{title}</span>
                {Icon && <Icon size={20} color={color} />}
            </div>
            <div>
                <span style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                    {value ?? '--'}
                </span>
                <span style={{ marginLeft: '0.25rem', color: 'var(--text-secondary)', fontSize: '1rem' }}>
                    {unit}
                </span>
            </div>
        </div>
    );
};

export default WeatherCard;
