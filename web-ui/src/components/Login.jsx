import { useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";

export function LoginPage() 
{
    let [login, setLogin] = useState("");
    let [password, setPassword] = useState("");
    let [state, setState] = useState("");
    let navigate = useNavigate()
    function get_user(e)
    {
        e.preventDefault();
        console.log(login, password);
        axios.post("api/login", {"login":login, "password":password}).then((resp) => {
                navigate("/chat")
        }).catch((reason) => {
            console.log(reason)
            setState(reason.code)
        })
    }

    return (<div className="login-block">
        <h2>Login</h2>
        <form  className="login-form">
            <input name="login" placeholder="login" value={login} onChange={(e)=> setLogin(e.target.value)}></input>
            <input name="password" type="password" placeholder="password" value={password} onChange={(e)=> setPassword(e.target.value)}></input>
            <button type="submit" onClick={get_user}>Login</button>
        </form>
        <p>{state}</p>
        <p>Not registered yet? <Link to={"/register"}>sign up</Link></p> 
    </div>);
}

export function RegisterPage() 
{
    let [login, setLogin] = useState("");
    let [password, setPassword] = useState("");
    let [name, setName] = useState("");
    let [state, setState] = useState("");
    let navigate = useNavigate()
    function get_user(e)
    {
        e.preventDefault();
        console.log(login, password, name);
        axios.post("api/register", {"login":login, "password":password, "name":name}).then((resp) => {
                navigate("/chat")
        }).catch((reason) => {
            console.log(reason)
            setState(reason.code)
        })
    }

    return (<div className="login-block">
        <h2>Register</h2>
        <form className="login-form">
            <input name="name" placeholder="name" value={name} onChange={(e)=> setName(e.target.value)}></input>
            <input name="login" placeholder="login" value={login} onChange={(e)=> setLogin(e.target.value)}></input>
            <input name="password" type="password" placeholder="password" value={password} onChange={(e)=> setPassword(e.target.value)}></input>
            <button type="submit" onClick={get_user}>Register</button>
        </form>
        <p>{state}</p>
        <p>Already registered? <Link to={"/login"}>sign in</Link></p> 
    </div>);
}