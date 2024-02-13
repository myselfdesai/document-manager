import React from 'react';
import { Navbar, Container, Button } from 'react-bootstrap';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const CustomNavbar = ({ isLoggedIn, handleLogout }) => {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');
  
  const logout = async (e) => {
    e.preventDefault();
    
    // Clear token from local storage
    localStorage.removeItem('token');
    
    const handleLogout = function (){
        localStorage.removeItem('token');
        //navigate("/login");
        window.location.href='/login';
    };

    try {
      await axios.post('http://localhost:8001/logout/', null, { headers: {
        Authorization: `Token ${token}`,
      }, });
      handleLogout();
    } catch (error) {
      console.error('Logout request failed:', error);
    }
  };

  return (
    <Navbar bg="dark" variant="dark" expand="lg" className="justify-content-between">
      <Container>
        <Navbar.Brand>Document Management</Navbar.Brand>
        <Navbar.Toggle aria-controls="navbar-collapse" />
        <Navbar.Collapse id="navbar-collapse" className="justify-content-end">
          <Navbar.Text>
            {isLoggedIn && (
              <>
                <Button onClick={logout} variant="secondary">Logout</Button>
              </>
            )}
          </Navbar.Text>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default CustomNavbar;
