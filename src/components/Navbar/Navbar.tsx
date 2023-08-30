import { useState } from "react";
import { NavLink } from "react-router-dom";
import "./Navbar.css";
import { UserAuth } from "../../context/AuthContext";
import { HamburgerIcon } from "@chakra-ui/icons";

export const Navbar = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const { user, logOut } = UserAuth();

  const handleSignOut = async () => {
    try {
      await logOut();
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <nav>
      <NavLink to="/tracking-log" className="title">
        Mailbi
      </NavLink>
      <HamburgerIcon
        className="menu"
        onClick={() => {
          setMenuOpen(!menuOpen);
        }}
      />
      <ul className={menuOpen ? "open" : ""}>
        <li>
          <NavLink to="/tracking-log">Tracking Log</NavLink>
        </li>
        <li>
          {user?.displayName ? (
            <NavLink to="/tracking-log" onClick={handleSignOut}>
              Log Out
            </NavLink>
          ) : (
            <NavLink to="/login">Login</NavLink>
          )}
        </li>
      </ul>
    </nav>
  );
};
