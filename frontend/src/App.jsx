import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { CloudRain, Droplets, Gauge, Thermometer, Wind, Sun, Battery, Wifi, Moon } from 'lucide-react';
import WeatherCard from './components/WeatherCard';
import HistoryChart from './components/HistoryChart';

function App() {
    const [current, setCurrent] = useState(null);
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [theme, setTheme] = useState('system'); // 'light', 'dark', 'system'

    // Initialize Theme
    useEffect(() => {
        const savedTheme = localStorage.getItem('theme') || 'system';
        setTheme(savedTheme);
        applyTheme(savedTheme);

        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        const handleSystemChange = (e) => {
            if (theme === 'system') {
                applyTheme('system');
            }
        };
        mediaQuery.addEventListener('change', handleSystemChange);
        return () => mediaQuery.removeEventListener('change', handleSystemChange);
    }, [theme]);

    const applyTheme = (mode) => {
        const root = document.documentElement;
        if (mode === 'dark') {
            root.setAttribute('data-theme', 'dark');
        } else if (mode === 'light') {
            root.setAttribute('data-theme', 'light');
        } else {
            // System
            const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            root.setAttribute('data-theme', systemDark ? 'dark' : 'light');
        }
    };

    const toggleTheme = () => {
        let newTheme = 'system';
        if (theme === 'system') {
            // If currently system, switch to opposite of system or just toggle logic
            // Simple toggle: Light -> Dark -> System
            newTheme = 'light';
        } else if (theme === 'light') {
            newTheme = 'dark';
        } else {
            newTheme = 'system';
        }

        // Let's do a simpler binary toggle + system logic if user wants.
        // For now: System -> Light -> Dark loop
        setTheme(newTheme);
        localStorage.setItem('theme', newTheme);
        applyTheme(newTheme);
    }

    const fetchData = async () => {
        try {
            // In dev, proxy handles /api -> localhost:8000
            // In prod/HA, we serve from same origin
            const [currRes, histRes] = await Promise.all([
                axios.get('/api/current'),
                axios.get('/api/history?hours=24')
            ]);
            setCurrent(currRes.data);
            setHistory(histRes.data);
        } catch (error) {
            console.error("Error fetching weather data:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 60000); // Poll every minute
        return () => clearInterval(interval);
    }, []);

    if (loading) {
        return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', color: 'var(--text-secondary)' }}>Loading Weather Station...</div>;
    }

    return (
        <div className="app">
            <header className="header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <div style={{ width: 40, height: 40, background: 'linear-gradient(135deg, #38bdf8, #818cf8)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <span style={{ fontSize: '1.2rem' }}>🌤️</span>
                    </div>
                    <h1>Weather Station</h1>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <button
                        onClick={toggleTheme}
                        className="glass-panel"
                        style={{
                            padding: '0.5rem',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.5rem',
                            color: 'var(--text-primary)'
                        }}
                    >
                        {theme === 'light' ? <Sun size={20} /> : theme === 'dark' ? <Moon size={20} /> : <span style={{ fontSize: '1.2rem' }}>🌓</span>}
                        <span style={{ fontSize: '0.8rem', textTransform: 'capitalize' }}>{theme}</span>
                    </button>
                    <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                        Updated: {current?.timestamp ? new Date(current.timestamp).toLocaleTimeString() : 'Never'}
                    </div>
                </div>
            </header>

            <main className="dashboard-grid">
                <WeatherCard
                    title="Temperature"
                    value={current?.temp_out?.toFixed(1)}
                    unit="°C"
                    icon={Thermometer}
                    color="#f87171"
                />
                <WeatherCard
                    title="Humidity"
                    value={current?.humidity_out}
                    unit="%"
                    icon={Droplets}
                    color="#60a5fa"
                />
                <WeatherCard
                    title="Wind Speed"
                    value={current?.wind_speed?.toFixed(1)}
                    unit="m/s"
                    icon={Wind}
                    color="#a78bfa"
                />
                <WeatherCard
                    title="Wind Direction"
                    value={current?.wind_dir}
                    unit="°"
                    icon={Wind}
                    color="#a78bfa"
                />
                <WeatherCard
                    title="Precipitation (Daily)"
                    value={current?.rain_daily?.toFixed(1)}
                    unit="mm"
                    icon={CloudRain}
                    color="#38bdf8"
                />
                <WeatherCard
                    title="Light Interval"
                    value={current?.solar_radiation?.toFixed(0)}
                    unit="W/m²"
                    icon={Sun}
                    color="#fbbf24"
                />
                <WeatherCard
                    title="UV Index"
                    value={current?.uv_index?.toFixed(1)}
                    unit=""
                    icon={Sun}
                    color="#fbbf24"
                />
                {/* Indoor/Extra */}
                <WeatherCard
                    title="Indoor Temp"
                    value={current?.temp_in?.toFixed(1)}
                    unit="°C"
                    icon={Thermometer}
                    color="#fca5a5"
                />

                {/* Charts */}
                <HistoryChart
                    data={history}
                    dataKey="temp_out"
                    color="#f87171"
                    title="Temperature History (24h)"
                    unit="°C"
                />
                <HistoryChart
                    data={history}
                    dataKey="wind_speed"
                    color="#a78bfa"
                    title="Wind Speed History (24h)"
                    unit="m/s"
                />
                <HistoryChart
                    data={history}
                    dataKey="rain_daily"
                    color="#38bdf8"
                    title="Precipitation History"
                    unit="mm"
                />

            </main>
        </div>
    );
}

export default App;
