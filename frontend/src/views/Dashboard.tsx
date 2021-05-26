import { Component } from 'react'

class Dashboard extends Component {
  token = localStorage.getItem("access")
  ws = new WebSocket(`ws://localhost:5000/ws/?token=${this.token}`)
  componentDidMount() {
    this.ws.onopen = () => {
      console.log('connected')
    }
    this.ws.onmessage = (message) => {
      console.log(JSON.parse(message.data))
    }

    this.ws.onclose = () => {
      console.log('disconnected')
    }
  }
  render() {
    return (<></>)
  }
}

export default Dashboard
