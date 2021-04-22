import { Logo } from "../assets/images/ShigotoLogo"
import { NavLink } from "react-router-dom"

import navigation from "../navigation"

type Props = {
    title: string,
    navLink: string,
    icon: JSX.Element
    key: number
}
const NavElement = ({title, navLink, icon, key}: Props) => {
    return ( 
        <NavLink exact to={navLink} key={key}  activeClassName="bg-gradient-to-r from-white to-purple-100 border-r-4 border-purple-500 border-r-4 border-purple-500" className="w-full font-bold uppercase text-purple-500 flex items-center p-4 my-2 transition-colors duration-200 justify-start dark:from-gray-700 dark:to-gray-800">
          <span className="text-left">
            {icon}
          </span>
          <span className="mx-4 text-sm font-normal">
            {title}
          </span>
        </NavLink>
    )
}

const renderSidebar = navigation.map((navli, idx) => {
        return <NavElement title={navli.title} key={idx} navLink={navli.navLink} icon={navli.icon}/>
    })
const Sidebar = () => {

    return (
  <div className="bg-white h-full rounded-2xl dark:bg-gray-700">
    <div className="flex items-center justify-center pt-6">
        <Logo/>
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
