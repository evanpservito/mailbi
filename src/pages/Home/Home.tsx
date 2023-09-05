import { Text } from "@chakra-ui/react";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { UserAuth } from "../../context/AuthContext";

const Home = () => {
  const { user } = UserAuth();
  const navigate = useNavigate();
  useEffect(() => {
    if (user != null) {
      navigate("/tracking-log");
    }
  }, [user]);

  return (
    <div>
      <Text as="b" fontSize="2xl">
        Mailbi Home
      </Text>
      <Text>Please login to continue.</Text>
    </div>
  );
};

export default Home;
