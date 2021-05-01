import axios from "axios"
import { useState } from "react"
import CronDropdown from "./CronSelect"
import { Switch } from "@headlessui/react"
import { connect } from "react-redux"
import {checkAuthenticated, load_user} from "../../redux/actions/auth/"

const CreateTask = () => {
  const [enabled, setEnabled] = useState(true)
  const [oneoff, setOneoff] = useState(false)
  const [taskName, setTaskName] = useState("")
  // eslint-disable-next-line
  const [crontab, setCrontab] = useState("")
  const [args, setArgs] = useState("")
  const [kwargs, setKwargs] = useState("")
  const userCrons = JSON.parse(localStorage.getItem("userData") || "{}").crontab
  const actualCrons = userCrons.map((item: any) => {
    return {
      value: [item.minute, item.hour, item.day_of_month, item.month_of_year].join(" "),
      id: item.id
    }
  })
  const handleSubmit = () => {
    const body = {
      name: taskName,
      crontab: crontab,
      args: args,
      kwargs: kwargs,
      one_off: oneoff,
      enabled: enabled
    }
    axios.post("/api/v1/task/", body)
      .then(res => { })
      .catch(err => { })
  }

  return (
    <div className="flex flex-col bg-white shadow-lg rounded-sm border border-gray-200">
      <header className="flex justify-between items-start mb-2">
      </header>
      <h2 className="text-md font-semibold text-gray-800 mb-2 ml-2">Create a task</h2>
      <div className="flex flex-nowrap">
        <form onSubmit={handleSubmit}>
          <div className="ml-2 mb-2">
            <label htmlFor="task" className="block text-sm font-medium text-gray-700">
              Task name:
          </label>
            <input
              type="text"
              name="task"
              id="task"
              placeholder="https://www.google.com"
              className="mt-1 mb-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
              onChange={(e) => setTaskName(e.target.value)}
              required
            />
            <label htmlFor="args" className="block text-sm font-medium text-gray-700">
              Args
          </label>
            <input
              type="text"
              name="args"
              id="args"
              placeholder="['arg1', 'arg2']"
              className="mt-1 mb-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
              onChange={(e) => setArgs(e.target.value)}
              required
            />
            <label htmlFor="kwargs" className="block text-sm font-medium text-gray-700">
              Kwargs
          </label>
            <input
              type="text"
              name="kwargs"
              id="kwargs"
              placeholder='{"argument": "value"}'
              className="mt-1 mb-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
              onChange={(e) => setKwargs(e.target.value)}
              required
            />
            <button
              type="submit"
              className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-purple-400 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
            >
              Submit
            </button>
          </div>
        </form>
        <div className="ml-2">
          <label htmlFor="kwargs" className="block text-sm font-medium text-gray-700">
            Select a crontab
          </label>
          <CronDropdown crons={actualCrons} />
          <div className="mt-8">
            <Switch.Group>
              <Switch.Label className="mr-4">Enabled</Switch.Label>
              <Switch
                checked={enabled}
                onChange={setEnabled}
                className={`${enabled ? "bg-purple-400" : "bg-gray-500"
                  } relative inline-flex items-center h-6 rounded-full w-11 transition-colors focus:outline-none`}
              >
                <span
                  className={`${enabled ? "translate-x-6" : "translate-x-1"
                    } inline-block w-4 h-4 transform bg-white rounded-full transition-transform`}
                />
              </Switch>
            </Switch.Group>
          </div>
          <div className="mt-10">
            <Switch.Group>
              <Switch.Label className="mr-4">One-off</Switch.Label>
              <Switch
                checked={oneoff}
                onChange={setOneoff}
                className={`${oneoff ? "bg-purple-400" : "bg-gray-500"
                  } relative inline-flex items-center h-6 rounded-full w-11 transition-colors focus:outline-none`}
              >
                <span
                  className={`${oneoff ? "translate-x-6" : "translate-x-1"
                    } inline-block w-4 h-4 transform bg-white rounded-full transition-transform`}
                />
              </Switch>
            </Switch.Group>
          </div>
        </div>
      </div>
    </div>
  )
}

export default connect(null, { checkAuthenticated, load_user })(CreateTask);
// export default CreateTask
