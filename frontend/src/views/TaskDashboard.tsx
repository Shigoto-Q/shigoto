import { Component } from 'react'
import TaskTable from "../components/tasks/TasksTable"
import Task from "../components/tasks/Task"
class Dashboard extends Component {
  render() {
    return (
      <div className="relative flex flex-col flex-1">
        <main>
          <div className="grid gap-4">
            <Task />
            <TaskTable />
          </div>
        </main>
      </div>
    )
  }
}

export default Dashboard
