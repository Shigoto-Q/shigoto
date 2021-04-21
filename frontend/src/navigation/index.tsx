import {CheckSquare, Cloud} from "react-feather"

const navigation = [
    {
        id: 'dashboard',
        title: 'Dashboard',
        icon: <Cloud />,
        navLink: '/dashboard'
    },
    {
        id: 'tasks',
        title: 'My Tasks',
        icon: <CheckSquare/>,
        navLink: '/dashboard/tasks'
    },
    {
        id: 'cron',
        title: 'Crontab Editor',
        icon: <CheckSquare/>,
        navLink: '/dashboard/cron'
    }
]

export default navigation
