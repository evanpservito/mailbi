import { Text } from "@chakra-ui/react";
import GoogleButton from "react-google-button";
import { UserAuth } from "../../context/AuthContext";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

const Login = () => {
  const { googleLogin, user } = UserAuth();
  const navigate = useNavigate();

  const handleGoogleLogin = async () => {
    try {
      await googleLogin();
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    if (user != null) {
      navigate("/tracking-log");
    }
  }, [user]);

  return (
    <div className="login">
      <Text as="b" fontSize="2xl">
        Login
      </Text>
      <GoogleButton onClick={handleGoogleLogin} />
    </div>
  );
};

export default Login;
