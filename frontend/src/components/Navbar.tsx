import { Link } from 'react-router-dom'

const Navbar = () => {
   return (
<>
{/* This example requires Tailwind CSS v2.0+ */}
<div className="relative bg-white">
  <div className="max-w-7xl mx-auto px-4 sm:px-6">
    <div className="flex justify-between items-center border-b-2 border-gray-100 py-6 md:justify-start md:space-x-10">
      <nav className="hidden md:flex space-x-10">
        <div className="relative">
          {/* Item active: "text-gray-900", Item inactive: "text-gray-500" */}
            <Link className="text-base font-medium text-gray-500 hover:text-gray-900" to="/">
            Solutions
            </Link>
        </div>
            <Link className="text-base font-medium text-gray-500 hover:text-gray-900" to="/pricing">
            Pricing
            </Link>
        <Link to="/" className="text-base font-medium text-gray-500 hover:text-gray-900">
          Documentation
        </Link>
      </nav>
      <div className="hidden md:flex items-center justify-end md:flex-1 lg:w-0">
        <Link to="/login" className="whitespace-nowrap text-base font-medium text-gray-500 hover:text-gray-900">
          Login
        </Link>
      </div>
      <div className="hidden md:flex items-center justify-end md:flex-1 lg:w-0">
        <Link to="/signup" className="whitespace-nowrap text-base font-medium text-gray-500 hover:text-gray-900">
          Sign up
        </Link>
      </div>
    </div>
  </div>
  {/*
    Mobile menu, show/hide based on mobile menu state.

    Entering: "duration-200 ease-out"
From: "opacity-0 scale-95"
To: "opacity-100 scale-100"
    Leaving: "duration-100 ease-in"
From: "opacity-100 scale-100"
To: "opacity-0 scale-95"
  */}
</div>
</>
   )
}

export default Navbar
