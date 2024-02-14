import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/CustomNavbar';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import FileVersions from './FileVersions';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));

  return (
    <Router>
      <Navbar isLoggedIn={isLoggedIn} />
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={isLoggedIn ? <Navigate to="/files" /> : <LoginForm  />} />
        <Route path="/register" element={<RegisterForm />} />
        <Route path="/files" element={isLoggedIn ? <FileVersions /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
