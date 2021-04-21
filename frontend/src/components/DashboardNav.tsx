import React from "react";
import { User, Settings } from 'react-feather'
import { Link } from 'react-router-dom'

const DashboardNav = () => {
  return (
        <div className="w-full px-4">
          <nav className="relative flex flex-wrap items-center justify-between px-2 py-3 bg-white-500 rounded shadow-md">
            <div className="container px-4 mx-auto flex flex-wrap items-center justify-between">  
              <div className="w-full relative flex justify-between lg:w-auto px-4 lg:static lg:block lg:justify-start">
                <input type="text" 
                        placeholder="Search task" 
                        className=""/>
              </div>
              <div
                className=
                  "lg:flex flex-grow items-center flex"
                id="example-navbar-info"
              >
                <ul className="flex flex-col lg:flex-row list-none lg:ml-auto">
                  <li className="nav-item">
                    <Link to=""
                      className="px-3 py-2 flex items-center text-xs uppercase font-bold leading-snug text-black hover:opacity-75"
                    >
                      <i className="fas fa-globe text-lg leading-lg text-black opacity-75">
                        <User/>
                      </i>
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link to=""
                      className="px-3 py-2 flex items-center text-xs uppercase font-bold leading-snug text-black hover:opacity-75"
                    >
                      <i className="fas fa-globe text-lg leading-lg text-black opacity-75">
                        <Settings/>
                      </i>
                    </Link>
                  </li>
                </ul>
              </div>
            </div>
          </nav>
        </div>
  );
}
export default DashboardNav
