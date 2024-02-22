import { Text } from "@chakra-ui/react";
import "./Footer.css";
import logo from "/mailbi logo v1.png";

const Footer = () => {
  return (
    <div className="footer">
      <Text as="b" fontSize="2xl">
        Happy Birthday MJ! 🎉
      </Text>
      <img src={logo} className="app-logo-footer" alt="logo" />
      <Text as="i">Mailbi Version 1.8.0</Text>
    </div>
  );
};

export default Footer;
