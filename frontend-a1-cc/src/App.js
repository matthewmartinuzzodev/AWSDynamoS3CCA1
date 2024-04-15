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

  //query functions/states
  const [queryMusic, setQueryMusicState] = useState({
    title: "",
    artist: "",
    year: ""
  });

  const [queryResults, setQueryResults] = useState()
  const handleQueryChange = (e) => {
    e.preventDefault();
    const value = e.target.value;
    setQueryMusicState({
      ...queryMusic,
      [e.target.name] : value
    });
  };
  const handleQuerySubmitForm = (e) => {
    e.preventDefault();
    const userData = {
      "type": "query",
      "title": queryMusic.title,
      "artist": queryMusic.artist,
      "year": queryMusic.year
    };
    // console.log(userData)
    axios.post("https://z1cu5gcf0d.execute-api.us-east-1.amazonaws.com/Production/queryMusicLambdaFunction", userData).then((response) => {
      setQueryResults(response.data.body.Response)
    });
  }

  //logout
  const handleLogout = (e) => {
    e.preventDefault();
    setLoginState(false);
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
          <div className='flex flex-col justify-center h-full mx-64'>
            <div className=''>
              <h1 className=' text-red-950 font-extrabold text-2xl'>User</h1>
              <div className='flex flex-row justify-center'>
                <p>welcome, you have logged in &nbsp;</p>
                <p className='text-violet-950 font-extrabold'>{username}</p>
              </div>
              <div>
                <button className='font-bold bg-slate-300 rounded-3xl text-white w-32 my-1' type='button' onClick={handleLogout}>Logout</button>
              </div>
            </div>
            <div className=''>
              <h1 className=' text-red-950 font-extrabold text-2xl'>Subscriptions</h1>
            </div>
            <div className='flex flex-col'>
              <div>
                <h1 className=' text-red-950 font-extrabold text-2xl'>Query</h1>
                <form>
                  <label>
                    <input className='border-2 border-slate-500 rounded my-1' placeholder='title' name='title' type='title' value={queryMusic.email} onChange={handleQueryChange} />
                    <br></br>
                    <input className='border-2 border-slate-500 rounded mb-1' placeholder='year' name='year' type='year' value={queryMusic.username} onChange={handleQueryChange} />
                    <br></br>
                    <input className='border-2 border-slate-500 rounded' placeholder='artist' name='artist' type='artist' value={queryMusic.password} onChange={handleQueryChange} />
                    <br></br>
                    <button className='font-bold bg-slate-500 rounded-3xl text-white w-32 my-1' type='button' onClick={handleQuerySubmitForm}>Query</button>
                  </label>
                </form>
              </div>
              <div> 
              {
                queryResults && queryResults.map((music, id) => {
                  return(
                    <div key={id} className=' border-2 m-2 flex flex-row'>
                      <div className=' flex-auto'>
                        <img src={`https://matthewmartinuzzoimagesbucket.s3.amazonaws.com/${music.title.replace("#", "%23")}.jpg`}></img>
                      </div>
                      <div className=' flex-auto self-center'>
                        <h1 className='font-bold'>{music.title}</h1>
                        <p>{music.artist}</p>
                        <p>{music.year}</p>
                        <button className='font-bold bg-slate-300 rounded-3xl text-white w-32 my-1' type='button'>Subscribe</button>
                      </div>
                      
                    </div>
                  );
                })
              }
              {
                queryResults && queryResults.length == 0 &&
                <p>No result is retrieved. Please query again</p>
              }
              </div>
            </div>
          </div>

          
          
        }
      </body>
    </div>
  );
}

export default App;
