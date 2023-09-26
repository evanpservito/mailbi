import { useState } from "react";
import { NavLink } from "react-router-dom";
import "./Navbar.css";
import { UserAuth } from "../../context/AuthContext";
import { HamburgerIcon } from "@chakra-ui/icons";
import { useNavigate } from "react-router-dom";
import logo from "/mailbi logo v1.png";

export const Navbar = () => {
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);
  const { user, logout } = UserAuth();

  const handleSignOut = async () => {
    try {
      await logout();
      navigate("/login");
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <nav>
      <NavLink to="/tracking-log" className="title">
        <img src={logo} className="app-logo" alt="logo" />
      </NavLink>
      <HamburgerIcon
        className="menu"
        onClick={() => {
          setMenuOpen(!menuOpen);
        }}
      />
      <ul className={menuOpen ? "open" : ""}>
        {user && (
          <li>
            <NavLink to="/tracking-log">Tracking Log</NavLink>
          </li>
        )}
        {user && (
          <li>
            <NavLink to="/package-status">Package Status</NavLink>
          </li>
        )}
        {user && (
          <li>
            <NavLink to="/add-mailbox">Add Mailbox</NavLink>
          </li>
        )}
        {user && (
          <li>
            <NavLink to="/custom-message">Custom Message</NavLink>
          </li>
        )}
        <li>
          {user && (
            <NavLink to="/tracking-log" onClick={handleSignOut}>
              Log Out
            </NavLink>
          )}
        </li>
      </ul>
    </nav>
  );
};
