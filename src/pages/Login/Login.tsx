import {
  Text,
  Input,
  Button,
  FormControl,
  FormLabel,
  Alert,
  AlertIcon,
  AlertDescription,
} from "@chakra-ui/react";
import { useState } from "react";
import { useNavigate, Navigate } from "react-router-dom";
import { UserAuth } from "../../context/AuthContext";
import logo from "/mailbi logo v1.png";

import "./Login.css";

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loggingIn, setLoggingIn] = useState(false);
  const { user, login } = UserAuth();

  if (user) {
    return <Navigate to="/tracking-log" />;
  }

  const handleLogin = async (e: any) => {
    e.preventDefault();
    setError("");
    try {
      setLoggingIn(true);
      await login(email, password);
      navigate("/tracking-log");
      setLoggingIn(false);
    } catch (error: any) {
      setLoggingIn(false);
      setError(error.message);
    }
  };

  return (
    <div className="login">
      <div className="login-side">
        <div className="login-form">
          <Text as="b" fontSize="4xl">
            Mailbi
          </Text>
          {error && (
            <Alert className="alert" variant="left-accent" status="error">
              <AlertIcon />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          <FormControl isRequired>
            <FormLabel>Email</FormLabel>
            <Input
              className="input-email"
              type="email"
              placeholder="Email"
              onChange={(e) => setEmail(e.target.value)}
            />
            <FormLabel>Password</FormLabel>
            <Input
              className="input-password"
              type="password"
              placeholder="Password"
              onChange={(e) => setPassword(e.target.value)}
              onSubmit={handleLogin}
            />
            <Button
              isLoading={loggingIn}
              isDisabled={email == "" || password == ""}
              loadingText="Logging in..."
              type="submit"
              width="10rem"
              onClick={handleLogin}
            >
              Log In
            </Button>
          </FormControl>
        </div>
      </div>
      <div className="logo-side">
        <img src={logo} className="app-logo" alt="logo" />
      </div>
    </div>
  );
};

export default Login;
