import { useEffect, useState } from "react"
import DataTable from 'react-data-table-component'
import { Link } from "react-router-dom"

const TaskLog = () => {
    const [tasks, setTasks] = useState<any[]>([])
    const [isSubscribed, setSubscribed] = useState(true)
    const token = localStorage.getItem("access")
    const handleWebsocket = () => {
        const ws = new WebSocket(`ws://localhost:8080?token=${token}`)
        ws.onopen = () => {
            console.log('connected')
        }
        ws.onmessage = (message) => {
            setTasks(JSON.parse(message.data))

        }

        ws.onclose = () => {
            console.log('disconnected')
            setSubscribed(false)
        }
    }

    useEffect(() => {
        if (isSubscribed)
            handleWebsocket()
        // eslint-disable-next-line
    }, ['a'])

    const columns = [
        {
            name: 'Task ID',
            selector: 'Task_id',
            sortable: true,
            cell: (row: any) => <Link className="text-blue-800" to={`${row.Task_id}/result`}>{row.Task_id}</Link>
        },
        {
            name: 'Task name',
            selector: 'Task_name',
            sortable: true,
        },
        {
            name: 'Status',
            selector: 'Status',
            sortable: true,
            width: "150px",
            cell: (row: any) => <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-${(row.Status === 'SUCCESS') ? ('green') : ((row.Status === 'FAILURE') ? 'red' : 'yellow')}-100 text-black-800`}>{row.Status}</span >
        },
        {
            name: 'Date done',
            selector: 'Date_done',

            sortable: true,
        },
        {
            name: 'Date created',
            selector: 'Date_created',
            sortable: true,
        },
        {
            name: 'Created by',
            selector: 'User_id',
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
