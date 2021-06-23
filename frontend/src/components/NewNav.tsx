import UserDropDown from "./UserDropDown";
import { connect } from "react-redux";
import { checkAuthenticated, load_user } from "../redux/actions/auth/";
import ThemeToggle from "./ThemeToggle"
type UserProps = {
    isAuthenticated: boolean;
    user: any;
};

const UserNav = ({ isAuthenticated, user }: UserProps) => {
    const userData = JSON.parse(user || "{}");

    return (
        <header className="sticky top-0 z-30 w-full shadow-lg bg-white dark:bg-gray-700 rounded-2xl">
            <div className="px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16 -mb-px">
                    <div className="flex">
                    </div>
                    <div className="flex items-center">
                        <ThemeToggle />
                        <hr className="w-px h-6 bg-gray-200 mx-3 dark:bg-gray-400" />
                        <UserDropDown user={userData.first_name}/>
                    </div>

                </div>
            </div>
        </header>

    )
}

const mapStateToProps = (state: any) => ({
    isAuthenticated: state.auth.isAuthenticated,
    user: state.auth.user,
});
export default connect(mapStateToProps, { checkAuthenticated, load_user })(UserNav);
