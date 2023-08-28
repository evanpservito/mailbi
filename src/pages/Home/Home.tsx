import { Text, Button } from "@chakra-ui/react";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div>
      <Text fontSize="2xl">Home</Text>
      <Button>
        <Link to="/login">Login with Google</Link>
      </Button>
    </div>
  );
};

export default Home;
