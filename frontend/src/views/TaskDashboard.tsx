import { Component } from 'react'
import CreateTask from "../components/tasks/Task"
import TaskLog from "../components/tasks/TaskLog"
import ActiveTasks from "../components/tasks/ActiveTasks"


class Dashboard extends Component {
  render() {
    return (
      <div className="relative flex flex-col flex-1">
        <main>
          <div className="grid grid-cols-3 gap-6">
            <CreateTask />
            <TaskLog />
            <ActiveTasks />
          </div>
        </main>
      </div>
    )
  }
}

export default Dashboard
