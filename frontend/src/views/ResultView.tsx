import { Component } from "react"
import { withRouter } from "react-router";
import { api } from "../api"
import ReactJson from 'react-json-view'


class ResultView extends Component<any, any> {
  constructor(props: any) {
    super(props)
    this.state = {
      id: "",
      data: {},
      loading: true,
    }
    this.downloadFile = this.downloadFile.bind(this)
  }
  componentDidMount() {
    const id = this.props?.match?.params.id;
    api.get(`/api/v1/task/${id}/result/`)
      .then(res => {
        this.setState({ data: res.data[0], loading: false })
      })
      .catch(err => { })
  }
  downloadFile = () => {
    const myData = JSON.parse(this.state.data.result.replace(/'/g, '"'))
    const fileName = this.state.data.task_id
    const json = JSON.stringify(myData);
    const blob = new Blob([json], { type: 'application/json' });
    const href = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = href;
    link.download = fileName + ".json";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
  render() {
    if (this.state.loading) {
      return (
        <div></div>
      )
    }
    return (
      <div className="relative flex flex-col flex-1">
        <main>
          <div className="flex flex-col bg-white shadow-lg rounded-sm border border-gray-200">
            <span className={`px-2 inline-flex text-xs leading-5 font-semibold text-center bg-${this.state.data.status === 'SUCCESS' ? 'green' : 'yellow'}-100 text-green-800`}>{this.state.data.status}</span>
            <span className="text-md font-semibold text-gray-800 mb-2 ml-1">{this.state.data.task_name}</span>
            <span className="text-sm font-italic text-gray-400 -mt-1 ml-3">{this.state.data.task_id}</span>
          </div>
          <div className="flex flex-col bg-white shadow-lg rounded-sm border border-gray-200">
            <button className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-purple-400 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-200" onClick={this.downloadFile}>Download result</button>
            <ReactJson collapsed={true} src={JSON.parse(this.state.data?.result?.replace(/'/g, '"'))} />
          </div>
        </main>
      </div>
    )
  }
}

export default withRouter(ResultView)
