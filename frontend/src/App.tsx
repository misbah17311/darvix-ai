import { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard/Dashboard';
import Login from './components/Auth/Login';

function App() {
  const [token, setToken] = useState(localStorage.getItem('darvix_token'));

  const handleLogin = (newToken: string) => {
    localStorage.setItem('darvix_token', newToken);
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('darvix_token');
    setToken(null);
  };

  if (!token) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard onLogout={handleLogout} />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
