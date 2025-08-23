import { useState } from 'react';
import '../static/login.css';
import { useNavigate} from 'react-router-dom';


function Login({ switchtoRegister }) {
  const [username, getusername] = useState('');
  const [password, getpassword] = useState('');
  const navigate=useNavigate();
  const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    const response = await fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    if (response.ok && data.access_token) {
      localStorage.setItem('token', data.access_token);  
      localStorage.setItem('userid' , data.user_id);
      alert('Login successful!');
      navigate('/home');  
    } 
    else {
      alert(data.message || 'Login failed');
    }
  } 
  catch (error) {
    console.error('Error:', error);
    alert('Server is not reachable. Is Flask running?');
  }
};


  return (
    <>
      <form onSubmit={handleSubmit}>
        <label>Login</label>
        <label>User name</label>
        <input
          type="text"
          placeholder="Enter the name"
          onChange={(e) => getusername(e.target.value)}
        />
        <br />
        <label>Password</label>
        <input
          type="password"
          placeholder="Enter password"
          onChange={(e) => getpassword(e.target.value)} 
        />
        <input type="submit" value="Login" />
        <p>
          If you don't have an account,{' '}
          <a href="#" onClick={(e) => { e.preventDefault(); switchtoRegister(); }}>
            Sign Up
          </a>
        </p>
      </form>
    </>
  );
}

export default Login;
