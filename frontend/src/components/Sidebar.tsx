import { NavLink } from "react-router-dom"
import logo from "../assets/images/logo_icon.png"

import navigation from "../navigation"

type Props = {
  title: string,
  navLink: string,
  icon: JSX.Element
  idx: string
}
const NavElement = ({ title, navLink, icon, idx }: Props) => {
  return (
    <NavLink exact to={navLink} activeClassName="bg-gradient-to-r from-white to-purple-200 border-r-4 border-purple-500 border-r-4 border-purple-500" className="w-full font-bold uppercase text-gray-500 flex items-center p-4 my-2 transition-colors duration-200 justify-start dark:from-gray-700 dark:to-gray-800">
      <span key={idx} className="text-left">
        {icon}
      </span>
      <span className="mx-4 text-sm font-medium font-normal">
        {title}
      </span>
    </NavLink>
  )
}

const renderSidebar = navigation.map((navli, idx) => {
  return <NavElement title={navli.title} idx={'test?-' + idx} navLink={navli.navLink} icon={navli.icon} />
})
const Sidebar = () => {

  return (
    <div className="h-screen bg-white rounded-2xl dark:bg-gray-700">
      <div className="flex items-center justify-center pt-6">
        <img src={logo} alt="logo" className="h-1/2"/>
        <span className="ml-3 text-3xl font-semibold text-gray-700">Shigoto</span>
      </div>
      <nav className="mt-6">
        <div>
          {renderSidebar}
        </div>
      </nav>
    </div>
  )
}

export default Sidebar
