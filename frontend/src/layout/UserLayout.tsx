import Sidebar from "../components/Sidebar"
import DashboardNav from "../components/DashboardNav"
import UserNav from "../components/NewNav"
import { useEffect } from "react"
import { connect } from "react-redux"
import { checkAuthenticated, load_user } from "../redux/actions/auth/"

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
        <div className="flex bg-gray-100 dark:bg-gray-800 h-screen overflow-hidden ">
            <div className="h-screen hidden lg:block my-4 ml-4 shadow-lg relative w-80">
                <Sidebar />
            </div>
            <div className="flex flex-col w-full pl-0 md:p-4 md:space-y-4">
                <UserNav />
                <div className="">
                    {props.children}
                </div>
            </div>
        </div>
    )
}

export default connect(null, { checkAuthenticated, load_user })(Layout);
