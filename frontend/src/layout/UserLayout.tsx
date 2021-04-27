import Sidebar from "../components/Sidebar"
import DashboardNav from "../components/DashboardNav"

const Layout = (props: any) => {
  return (
    <div className="flex">
      <div className="absolute shadow-lg relative w-80">
        <Sidebar />
      </div>
      <div className="flex flex-col h-screen w-screen">
        <DashboardNav />
        <div className="ml-10 mt-10 mr-10">
          {props.children}
        </div>
      </div>
    </div>
  )
}

export default Layout
