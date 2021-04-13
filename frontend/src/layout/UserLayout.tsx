import Footer from "../components/Footer"
import Sidebar from "../components/Sidebar"
import DashboardNav from "../components/DashboardNav"

const Layout = (props: any) => {
    return (
        <div className="flex">
        
        <div className="h-screen shadow-lg relative w-80">
                <Sidebar /> 
                </div>
            <DashboardNav/>
            {props.children}
        </div>
    )
}

export default Layout
