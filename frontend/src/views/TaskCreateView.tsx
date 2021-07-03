import { Fragment, useState } from 'react'
import { Listbox, Transition } from '@headlessui/react'
import { Check, Menu, Calendar } from 'react-feather'
import DropdownMenu from "../components/generic/DropdownMenu";

const taskTypes = [
    {
        id: 1,
        name: 'Custom endpoint request',
        value: 'custom_endpoint'
    },
    {
        id: 2,
        name: 'Job',
        value: 'k8s_job'
    }
]

function classNames(...classes: any) {
    return classes.filter(Boolean).join(' ')
}

const TaskCreate = () => {



    const [selected, setSelected] = useState(taskTypes[0])

    return (
        <DropdownMenu selected={selected} setSelected={setSelected} options={taskTypes} />

    )

}


export default TaskCreate
