import { Component } from "react"
import { withRouter } from "react-router";
import { api } from "../api"
import ReactJson from 'react-json-view'

interface MyState {
  id: string,
  data: any
}

interface ResultProps {
  data: any
  id: string,
}

class ResultView extends Component<any, any> {
  constructor(props: any) {
    super(props)
    this.state = {
      id: "",
      data: {},
      loading: true,
    }
  }
  componentDidMount() {
    const id = this.props?.match?.params.id;
    api.get(`/api/v1/task/${id}/result/`)
      .then(res => {
        this.setState({ data: res.data[0], loading: false })
      })
      .catch(err => { })
  }
  render() {
    console.log(this.state.data)
    if (this.state.loading) {
      return (
        <div></div>
      )
    }
    return (
      <div className="relative flex flex-col flex-1">
        <main>
          <div className="grid gap-4">
            <span>{this.state.data.task_name}</span>
            <span>{this.state.data.task_id}</span>
            <span>{this.state.data.status}</span>
            <ReactJson src={JSON.parse(this.state.data.result.replace(/'/g, '"'))}/>
          </div>
        </main>
      </div>
    )
  }
}

export default withRouter(ResultView)
