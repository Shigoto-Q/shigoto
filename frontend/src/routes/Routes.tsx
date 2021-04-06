import {BrowserRouter as Router, Switch, Route} from "react-router-dom"
import Login from '../components/Login'
import Layout from "../layout/Layout"
import Pricing from "../views/PricingPage"
import Dashboard from "../views/Dashboard"

const Routes = () => {

    return (
        <Router>
            <Layout>
                <Switch>
                   <Route exact path='/' component={Login} /> 
                   <Route exact path='/pricing' component={Pricing} /> 
                   <Route exact path='/dashboard' component={Dashboard} /> 
                </Switch>
            </Layout>
        </Router>
    )
}

export default Routes
