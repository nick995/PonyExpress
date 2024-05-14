import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth, useApi } from "../hooks";

import Button from "./Button";
import FormInput from "./FormInput";

function Error({ message }) {
  if (message === "") {
    return <></>;
  }
  return (
    <div className="text-red-300 text-xs">
      {message}
    </div>
  );
}

function RegistrationLink() {
  return (
    <div className="pt-8 flex flex-col">
      <div className="text-xs">
        need an account?
      </div>
      <Link to="/registration">
        <Button className="mt-1 w-full">
          register
        </Button>
      </Link>
    </div>
  );
}

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const { login } = useAuth();

  const disabled = username === "" || password === "";

  const api = useApi();

  // fake

  const onSubmit = (e) => {
    e.preventDefault();


    api.postForm("/auth/token", { username, password })
    .then((response) => {
      if (response.ok) {
        console.log(response);
        response.json().then(login).then(
          () => navigate("/chats")
          
        );
      } else if (response.status === 401) {
        console.log(response);
        response.json().then((data) => {
          setError(data.detail.error_description);
        });
      } else {
        setError("error logging in");
      }
    });
  }

  return (
    <div className="max-w-96 mx-auto py-8 px-4 bg-white">
      <form onSubmit={onSubmit}>
        <FormInput type="text" name="username" setter={setUsername} />
        <FormInput type="password" name="password" setter={setPassword} />
        <Button className="w-full" type="submit" disabled={disabled}>
          login
        </Button>
        <Error message={error} />
      </form>
      <RegistrationLink />
    </div>
  );
}

export default Login;
