import {CheckSquare, Calendar} from "react-feather"

const navigation = [
    {
        id: 'tasks',
        title: 'My Tasks',
        icon: <CheckSquare/>,
        navLink: '/dashboard/tasks'
    },
    {
        id: 'cron',
        title: 'Scheduler',
        icon: <Calendar/>,
        navLink: '/dashboard/scheduler'
    }
]

export default navigation
