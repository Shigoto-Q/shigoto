import Sidebar from "../components/Sidebar"
import DashboardNav from "../components/DashboardNav"
import { useEffect } from "react"
import { connect } from "react-redux"
import {checkAuthenticated, load_user} from "../services/auth/auth"

const Layout = (props: any) => {
  useEffect(() => {
    const fetchData = async () => {
      try {
        await props.checkAuthenticated();
        await props.load_user();
      } catch (err) {
      }
    };
    fetchData();
  }, [props]);
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

export default connect(null, { checkAuthenticated, load_user })(Layout);
// export default Layout
