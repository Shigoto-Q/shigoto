

const Navbar = () => {
   return (
<>
{/* This example requires Tailwind CSS v2.0+ */}
<div className="relative bg-white">
  <div className="max-w-7xl mx-auto px-4 sm:px-6">
    <div className="flex justify-between items-center border-b-2 border-gray-100 py-6 md:justify-start md:space-x-10">
      <div className="flex justify-start lg:w-0 lg:flex-1">
        <a href="#">
          <span className="sr-only">Workflow</span>
        </a>
      </div>
      <div className="-mr-2 -my-2 md:hidden">
        <button type="button" className="bg-white rounded-md p-2 inline-flex items-center justify-center text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500" aria-expanded="false">
          <span className="sr-only">Open menu</span>
          {/* Heroicon name: outline/menu */}
          <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>
      <nav className="hidden md:flex space-x-10">
        <div className="relative">
          {/* Item active: "text-gray-900", Item inactive: "text-gray-500" */}
          <button type="button" className="text-gray-500 group bg-white rounded-md inline-flex items-center text-base font-medium hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500" aria-expanded="false">
            <span>Solutions</span>
            {/*
        Heroicon name: solid/chevron-down

        Item active: "text-gray-600", Item inactive: "text-gray-400"
      */}
          </button>
        </div>
        <a href="#" className="text-base font-medium text-gray-500 hover:text-gray-900">
          Pricing
        </a>
        <a href="#" className="text-base font-medium text-gray-500 hover:text-gray-900">
          Documentation
        </a>
      </nav>
      <div className="hidden md:flex items-center justify-end md:flex-1 lg:w-0">
        <a href="#" className="whitespace-nowrap text-base font-medium text-gray-500 hover:text-gray-900">
          Sign up
        </a>
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
