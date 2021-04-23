import Sidebar from "../components/Sidebar"
import DashboardNav from "../components/DashboardNav"

const Layout = (props: any) => {
    return (
        <div className="flex">
        <div className="h-screen shadow-lg relative w-80">
                <Sidebar /> 
                </div>
            <div className="flex flex-col h-screen w-screen">
                <DashboardNav/>
                {props.children}
            </div>

        </div>
    )
}

export default Layout
