import { Component } from 'react'
import axios from 'axios'

class Dashboard extends Component {
    componentWillMount() {
        axios.get('/api/v1/cron/')
            .then(res => {
                this.setState({ prices: res.data })
            })
    }
    render() {
        return (<></>)
    }
}

export default Dashboard
