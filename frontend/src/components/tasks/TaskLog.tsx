import { useEffect, useState } from "react"
import { CheckCircle, XCircle } from "react-feather"
import DataTable from 'react-data-table-component'

const TaskLog = () => {
  const [tasks, setTasks] = useState<any[]>([])
  const ws = new WebSocket('ws://localhost:8000/ws/task/')
  const handleWebocket = () => {
    let data = {
      test: "da"
    }
    ws.onopen = () => {
      console.log('connected')
      ws.send(JSON.stringify(data))
    }
    ws.onmessage = (message) => {
      //console.log(JSON.parse(message.data))
      setTasks(JSON.parse(message.data))
    }

    ws.onclose = () => {
      console.log('disconnected')
    }
  }
  useEffect(() => {
    handleWebocket()
  }, [])
  const columns = [
    {
      name: 'Task ID',
      selector: 'task_id',
      sortable: true,
    },
    {
      name: 'Task name',
      selector: 'task_name',
      sortable: true,
    },
    {
      name: 'Status',
      selector: 'status',
      sortable: true,
      width: "150px",
      cell: (row: any) => <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-${row.status === 'SUCCESS' ? 'green' : 'yellow'}-100 text-green-800`}>{row.status}</span >
    },
    {
      name: 'Date done',
      selector: 'date_done',
      sortable: true,
    },
    {
      name: 'Date created',
      selector: 'date_created',
      sortable: true,
    },
    {
      name: 'Created by',
      selector: 'user',
      sortable: true,
    },
  ];
  return (
    <div className="flex flex-col">
      <div className="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div className="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
          <div className="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
            <DataTable title="Tasks logs" columns={columns} data={tasks} pagination />
          </div>
        </div>
      </div>
    </div>
  )
}

export default TaskLog
