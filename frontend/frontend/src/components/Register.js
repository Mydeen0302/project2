import '../static/login.css';
import { useState } from 'react';

function Register({ switchtoLogin }) {
  const [username, setusername] = useState('');
  const [password, setpassword] = useState('');
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const message = await response.text(); 
      console.log(message);
      alert(message);
    } catch (error) {
      console.error('Error:', error);
      alert('Server is not reachable. Is Flask running?');
    }
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <label>Register</label>
        <label>User name</label>
        <input
          type="text"
          placeholder="Enter the name"
          value={username}
          onChange={(e) => setusername(e.target.value)}
        />
        <br />
        <label>Password</label>
        <input
          type="password"
          placeholder="Enter password"
          value={password}
          onChange={(e) => setpassword(e.target.value)}
        />
        <input type="submit" value="Register" />
        <p>
          If you already have an account{' '}
          <a
            href="#"
            onClick={(e) => {
              e.preventDefault();
              switchtoLogin();
            }}
          >
            Sign in
          </a>
        </p>
      </form>
    </>
  );
}

export default Register;
