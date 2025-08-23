import React, { useState } from "react";
import Login from "./Login";
import Register from "./Register";
function Auth()
{
    const[showLogin,setShowLogin] =useState(true);
    return(
        <>
        {showLogin ?
        (<Login switchtoRegister={()=>setShowLogin(false)}/>):
        (<Register switchtoLogin={()=>setShowLogin(true)}/>)    
        }
        </>
    );
}
export default Auth;