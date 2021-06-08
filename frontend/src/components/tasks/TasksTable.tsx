import { api } from "../../api/";
import { useState, useEffect } from "react";
import { CheckCircle, XCircle } from "react-feather";
import { Redirect } from "react-router-dom"
import { runTask } from "../../redux/actions/task/"
import { connect } from "react-redux"
import { checkAuthenticated } from "../../redux/actions/auth/"
type TaskProps = {
  isAuthenticated?: boolean,
  runTask: any,
}
const TaskTable = ({ isAuthenticated, runTask }: TaskProps) => {
  const [tasks, setTasks] = useState<any[]>([]);
  const getUserTasks = () => {
    api
      .get("/api/v1/task/")
      .then((res) => {
        setTasks(res.data);
      })
      .catch((err) => { });
  };
  const handleRun = (id: number, event: any) => {
    event.preventDefault()
    runTask(id)
  }
  useEffect(() => {
    getUserTasks();
  }, []);
  if (!isAuthenticated) {
    return <Redirect to="/login" />
  }
  return (
    <div className="flex flex-col">
      <div className="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div className="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
          <div className="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Task Name
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Crontab
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Status
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    One-off
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Enabled
                  </th>
                  <th scope="col" className="relative px-6 py-3">
                    <span className="sr-only">Edit</span>
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {tasks.map((task) => (
                  <tr key={task.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10">
                          <span className="h-10 w-10 rounded-full">
                            {task.id}
                          </span>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">
                            {task.name}
                          </div>
                          <div className="text-sm text-gray-500">
                            Total run count: {task.total_run_count}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {task.crontab
                          ? task.crontab.minute +
                          " " +
                          task.crontab.hour +
                          " " +
                          task.crontab.day_of_month +
                          " " +
                          task.crontab.month_of_year +
                          " " +
                          task.crontab.day_of_week
                          : task.interval}
                      </div>
                      <div className="text-sm text-gray-500"></div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        Active
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {task.one_off ? <CheckCircle /> : <XCircle />}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {task.enabled ? <CheckCircle /> : <XCircle />}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        type="submit"
                        className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-purple-400 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
                        onClick={(e) => handleRun(task.id, e)}
                      >
                        Run
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

const mapStateToProps = (state: any) => ({
  isAuthenticated: state.auth.isAuthenticated,
})

export default connect(mapStateToProps, { checkAuthenticated, runTask })(TaskTable);
