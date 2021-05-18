import { CheckSquare, Calendar, Activity } from "react-feather"

const navigation = [
  {
    id: 'tasks',
    title: 'My Tasks',
    icon: <CheckSquare />,
    navLink: '/dashboard/tasks'
  },
  {
    id: 'taskLogs',
    title: 'Cron logs',
    icon: <Activity />,
    navLink: '/dashboard/logs'
  },
  {
    id: 'cron',
    title: 'Scheduler',
    icon: <Calendar />,
    navLink: '/dashboard/scheduler'
  }
]

export default navigation
