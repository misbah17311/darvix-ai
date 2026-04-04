import { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard/Dashboard';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';

function App() {
  const [token, setToken] = useState(localStorage.getItem('darvix_token'));
  const [showRegister, setShowRegister] = useState(false);

  const handleLogin = (newToken: string) => {
    localStorage.setItem('darvix_token', newToken);
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('darvix_token');
    setToken(null);
  };

  if (!token) {
    if (showRegister) {
      return (
        <Register
          onRegistered={() => setShowRegister(false)}
          onBackToLogin={() => setShowRegister(false)}
        />
      );
    }
    return <Login onLogin={handleLogin} onShowRegister={() => setShowRegister(true)} />;
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
