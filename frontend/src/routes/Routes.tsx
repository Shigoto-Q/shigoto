import {BrowserRouter as Router, Switch, Route} from "react-router-dom"
import Layout from "../layout/Layout"
import UserLayout from "../layout/UserLayout"
import Pricing from "../views/PricingPage"
import Dashboard from "../views/Dashboard"
import Home from "../views/HomePage"

const Routes = () => {

    return (
        <Router>
            <Switch>
            <Route path='/dashboard/:path?'>
            <UserLayout>
                <Switch>
                   <Route exact path='/dashboard' component={Dashboard} /> 
                   <Route exact path='/dashboard/tasks' component={Dashboard} /> 
                </Switch>
            </UserLayout>
            </Route>
            <Route>
            <Layout>
                <Switch>
                   <Route exact path='/' component={Home} /> 
                   <Route exact path='/pricing' component={Pricing} /> 
                </Switch>
            </Layout>
            </Route>
            </Switch>
        </Router>
    )
}

export default Routes
