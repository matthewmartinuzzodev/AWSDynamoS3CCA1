import './App.css';
import axios from 'axios';
import React, { useState } from "react";


function App() {

  //login states/functions
  const [data, setData] = useState({
    email: "",
    password: ""
  });
  const [loginState, setLoginState] = useState()
  const [failedLogin, setFailedLoginState] = useState(false)
  const [username, setUsername] = useState("")
  const handleChange = (e) => {
    e.preventDefault();
    const value = e.target.value;
    setData({
      ...data,
      [e.target.name] : value
    });
  };
  const handleSubmitLogin = (e) => {
    e.preventDefault();
    const userData = {
      "type": "validate",
      "user" : {
        "email": data.email,
        "password": data.password
      }
    };
    if (data.email=="" | data.password==""){
      setFailedLoginState(true);
    }
    else {
      axios.post("https://lguwvr27be.execute-api.us-east-1.amazonaws.com/Production/loginUserLambdaFunctions", userData).then((response) => {
        // console.log(userData)
        console.log("response data: ", response.data)
        setLoginState(response.data.body.Valid);
        setUsername(response.data.body.username)
  
        if (!response.data.body.Valid){
          setFailedLoginState(true);
        }
      });
    }

  };

  //register states/functions
  const [dataRegister, setDataRegister] = useState({
    email: "",
    username: "",
    password: ""
  });
  const [registerState, setRegisterState] = useState(false)
  const [invalidRegister, setInvalidRegisterState] = useState(false)
  const [registerNotComplete, setRegisterNotComplete] = useState(false)
  const handleSubmitRegister = (e) => {
    e.preventDefault();
    setRegisterState(true);
  }
  const handleChangeRegisterForm = (e) => {
    e.preventDefault();
    const value = e.target.value;
    setDataRegister({
      ...dataRegister,
      [e.target.name] : value
    });
  };
  const handleSubmitRegisterForm = (e) => {
    e.preventDefault();
    const userData = {
      "type": "register",
      "user" : {
        "email": dataRegister.email,
        "user_name": dataRegister.username,
        "password": dataRegister.password
      }
    };
    if (dataRegister.email=="" | dataRegister.password=="" | dataRegister.username==""){
      setRegisterNotComplete(true);
    }
    else {
      axios.post("https://lguwvr27be.execute-api.us-east-1.amazonaws.com/Production/loginUserLambdaFunctions", userData).then((response) => {
        if (response.data.body.Response == "User successfully added to database") {
          // console.log(userData)
          // console.log("response data: "  + response.data)
          setRegisterState(false)
          alert(response.data.body.Response);
        }
        else {
          setInvalidRegisterState(true)
          setRegisterNotComplete(false)
        }
      });
    }
  }

  return (
    <div className="App">
      <head>
        <link href="./output.css" rel="stylesheet">
        </link>
      </head>
      <body>
        {
          !loginState && !registerState &&
          <form>
            <label>
              <p className='font-bold text-purple-950 text-3xl'>Login Here:</p>
              <br></br>
              <input className='border-2 border-slate-500 rounded my-1' placeholder='email' name='email' type='email' value={data.email} onChange={handleChange} />
              <br></br>
              <input className='border-2 border-slate-500 rounded' placeholder='password' name='password' type='password' value={data.password} onChange={handleChange} />
              <br></br>
              {
                failedLogin &&
                <p className=' text-red-500'>email or password is invalid</p>
              }
              <button className='font-bold bg-slate-500 rounded-3xl text-white w-32 my-1' type='submit' onClick={handleSubmitLogin}>Login</button>
              <br></br>
              <button className='font-bold bg-slate-500 rounded-3xl text-white w-32' type='button' onClick={handleSubmitRegister}>Register</button>
            </label>
         </form>
        }
        {
          registerState &&
          <form>
              <label>
                <p className='font-bold text-purple-950 text-3xl'>Register Here:</p>
                <br></br>
                <input className='border-2 border-slate-500 rounded my-1' placeholder='email' name='email' type='email' value={dataRegister.email} onChange={handleChangeRegisterForm} />
                <br></br>
                <input className='border-2 border-slate-500 rounded mb-1' placeholder='username' name='username' type='username' value={dataRegister.username} onChange={handleChangeRegisterForm} />
                <br></br>
                <input className='border-2 border-slate-500 rounded' placeholder='password' name='password' type='password' value={dataRegister.password} onChange={handleChangeRegisterForm} />
                <br></br>
                {
                  invalidRegister &&
                  <p className=' text-red-500'>The email already exists</p>
                }
                {
                  registerNotComplete &&
                  <p className=' text-red-500'>Please fill in all fields</p>
                }
                <button className='font-bold bg-slate-500 rounded-3xl text-white w-32 my-1' type='button' onClick={handleSubmitRegisterForm}>Register</button>
            </label>
          </form>
        }
        {
          loginState &&
          <div className='flex flex-row justify-center'>
            <p>welcome, you have logged in &nbsp;</p>
            <p className='text-violet-950 font-extrabold'>{username}</p>
          </div>
          
        }
      </body>
    </div>
  );
}

export default App;
