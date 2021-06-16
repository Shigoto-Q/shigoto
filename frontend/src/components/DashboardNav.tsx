import { Redirect } from "react-router-dom"
import { Settings, Moon } from "react-feather";
import { Link } from "react-router-dom";
import UserDropDown from "./UserDropDown";

import { connect } from "react-redux";
import { checkAuthenticated, load_user } from "../redux/actions/auth/";

type TaskProps = {
  isAuthenticated: boolean;
  user: any;
};

const DashboardNav = ({ isAuthenticated, user }: TaskProps) => {
  if (!isAuthenticated) {
    return <Redirect to="/" />
  }
  const userData = JSON.parse(user || "{}");
  return (
    <div className="w-full px-4">
      <nav className="relative flex flex-wrap items-center justify-between px-2 py-3 bg-white-500 dark:bg-gray-700 rounded shadow-md">
        <div className="container px-4 mx-auto flex flex-wrap items-center justify-between">
          <div
            className="lg:flex flex-grow items-center flex"
            id="example-navbar-info"
          >
            <p className="px-3 py-2 flex items-center font-mono text-sm uppercase font-bold leading-snug text-purple-400 hover:opacity-75">
              {" "}
              Total tasks: {userData?.task?.length}{" "}
            </p>
            <p className="px-3 py-2 flex items-center font-mono text-sm uppercase font-bold leading-snug text-purple-400 hover:opacity-75">
              {" "}
              Active tasks: 0{" "}
            </p>
            <p className="px-3 py-2 flex items-center font-mono text-sm uppercase font-bold leading-snug text-purple-400 hover:opacity-75">
              {" "}
              Failed tasks: 0{" "}
            </p>
            <p className="px-3 py-2 flex items-center font-mono text-sm uppercase font-bold leading-snug text-purple-400 hover:opacity-75">
              {" "}
              Finished tasks: 0{" "}
            </p>

            <ul className="flex flex-col lg:flex-row list-none lg:ml-auto">
              <li className="nav-item">
                <div className="px-3 py-2 flex items-center text-xs uppercase font-bold leading-snug text-black hover:opacity-75">
                  <Moon />
                </div>
              </li>
              <li className="nav-item">
                <p className="mt-1 px-3 py-2 flex items-center text-sm font-bold leading-snug text-black hover:opacity-75">
                  {userData.first_name} {userData.last_name}
                </p>
              </li>
              <li className="nav-item">
                <div className="px-3 py-2 flex items-center text-xs uppercase font-bold leading-snug text-black hover:opacity-75">
                  <UserDropDown />
                </div>
              </li>
              <li className="nav-item">
                <Link
                  to="/dashboard/profile-settings/"
                  className="px-3 py-2 flex items-center text-xs uppercase font-bold leading-snug text-black hover:opacity-75"
                >
                  <i className="fas fa-globe text-lg leading-lg text-black opacity-75">
                    <Settings />
                  </i>
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
};
const mapStateToProps = (state: any) => ({
  isAuthenticated: state.auth.isAuthenticated,
  user: state.auth.user,
});
export default connect(mapStateToProps, { checkAuthenticated, load_user })(DashboardNav);

