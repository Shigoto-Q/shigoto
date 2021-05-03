import { Link } from "react-router-dom";
import logo from "../assets/images/logo.png";
import logoIcon from "../assets/images/logo_icon.png";
import { motion } from "framer-motion";

const Navbar = () => {
  return (
    <div className="container mx-auto flex flex-wrap p-5 flex-col md:flex-row items-center">
      <Link
        to="/"
        className="flex title-font font-medium items-center text-gray-900 mb-4 md:mb-0"
      >
        <img src={logoIcon} alt="logo" className="h-16" />{" "}
        <span className="ml-3 text-xl text-gray-700">Shigoto</span>
      </Link>
      <nav className="md:mr-auto md:ml-4 md:py-1 md:pl-4 md:border-l md:border-gray-400	flex flex-wrap items-center text-base justify-center">
        <Link to="/pricing" className="mr-5 hover:text-gray-900">
          Pricing
        </Link>
        <Link to="/features" className="mr-5 hover:text-gray-900">
          Features
        </Link>
        <Link to="/docs" className="mr-5 hover:text-gray-900">
          Documentation
        </Link>
      </nav>
      <motion.button whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
        <Link
          to="/login"
          className="inline-flex items-center border-0 py-1 px-3 focus:outline-none hover:bg-gray-200 rounded text-base mt-4 md:mt-0"
        >
          Sign in
          <svg
            fill="none"
            stroke="currentColor"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            className="w-4 h-4 ml-1"
            viewBox="0 0 24 24"
          >
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </Link>
      </motion.button>
    </div>
  );
};

export default Navbar;
