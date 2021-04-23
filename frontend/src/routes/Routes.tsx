import {BrowserRouter as Router, Switch, Route, useLocation} from "react-router-dom"
import Layout from "../layout/Layout"
import UserLayout from "../layout/UserLayout"
import Pricing from "../views/PricingPage"
import Dashboard from "../views/Dashboard"
import Login from "../components/Login"
import Home from "../views/HomePage"
import SignUp from "../components/SignUp"
import CronDash from "../views/DashboardCron"
import {AnimatePresence} from 'framer-motion'

const Routes = () => {
    return (
        <Router>
            <AnimatePresence exitBeforeEnter>
            <Switch >
            <Route path='/dashboard/:path?'>
            <UserLayout>
                <Switch> 
                   <Route exact path='/dashboard' component={Dashboard} /> 
                   <Route exact path='/dashboard/tasks' component={Dashboard} /> 
                   <Route exact path='/dashboard/cron' component = {CronDash} />
                </Switch>
            </UserLayout>
            </Route>
            <Route>
            <Layout>
                <Switch>
                   <Route exact path='/' component={Home} /> 
                   <Route exact path='/login' component={Login} /> 
                   <Route exact path='/signup' component={SignUp} /> 
                   <Route exact path='/pricing' component={Pricing} /> 
                </Switch>
            </Layout>
            </Route>
            </Switch>
            </AnimatePresence>
        </Router>
    )
}

export default Routes
