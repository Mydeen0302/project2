  import { useState, useEffect } from "react";
 import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
  import Auth from "./components/Auth";
  import Homepage from "./components/HomePage"
  function App() {
   
  return (
    <Router>
        <Routes>
          <Route path='/' element={<Auth/>} />
          <Route path='/home' element={<Homepage/>} />
      
    </Routes>
    </Router>
  )
  }

  export default App;
