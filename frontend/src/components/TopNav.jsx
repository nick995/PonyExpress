import { NavLink } from "react-router-dom";
import { useAuth } from "../context/auth";
import { useUser } from "../context/user";

function NavItem({ to, name, right }) {
  const className = [
    "bg-[#FFFBE9]",
    "py-2 px-4",
    "hover:bg-[#E3CAA5]",
    right ? "border-l-2" : "border-r-2"
  ].join(" ")

  const getClassName = ({ isActive }) => (
    isActive ? className + " bg-[#E3CAA5]" : className
  );

  return (
    <NavLink to={to} className={getClassName}>
      {name}
    </NavLink>
  );
}

function AuthenticatedNavItems() {
  const user = useUser();

  return (
    <>
      <NavItem to="/" name="pony express" />
      <div className="flex-1" />
      <NavItem to="/profile" name={user?.username} right />
    </>
  );
}

function UnauthenticatedNavItems() {
  return (
    <>
      <NavItem to="/" name="pony express" />
      <div className="flex-1" />
      <NavItem to="/login" name="login" right />
    </>
  );
}


function TopNav() {
  const { isLoggedIn } = useAuth();

  return (
    <nav className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-2 bg-white">
      {isLoggedIn ?
        <AuthenticatedNavItems /> :
        <UnauthenticatedNavItems />
      }
    </nav>
  );
}

export default TopNav;