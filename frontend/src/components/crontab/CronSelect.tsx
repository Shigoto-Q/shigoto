import { Fragment, useState } from 'react'
import { Listbox, Transition } from '@headlessui/react'
import { Check, Menu, Calendar } from 'react-feather'
import Crontab from "../crontab/Crontab"
import DropdownMenu from "../generic/DropdownMenu";

const crontabs = [
  {
    id: 1,
    name: 'At minute 10',
    value: '10 * * * *'
  },
  {
    id: 2,
    name: 'Every minute',
    value: '* * * *'
  },
  {
    id: 3,
    name: ' At every 2nd minute',
    value: '*/2 * * * *'
  },
  {
    id: 4,
    name: 'At every 2nd minute from 1 through 59',
    value: '1-59/2 * * * *'
  },
  {
    id: 5,
    name: 'At every 10th minute',
    value: '*/10 * * * *'
  },
  {
    id: 6,
    name: ' At every 6th minute',
    value: '*/6 * * * *'
  },
  {
    id: 7,
    name: 'At every 5th minute',
    value: '*/5 * * * * '
  },
  {
    id: 8,
    name: 'At 00:00 on Friday',
    value: '0 0 * * FRI '
  },
  {
    id: 9,
    name: 'At minute 0 past every hour from 9 through 17',
    value: '0 9-17 * * *'
  },
  {
    id: 10,
    name: 'At 00:00 every day-of-week from Monday through Friday',
    value: '0 0 * * 1-5 '
  },
]

function classNames(...classes: any) {
  return classes.filter(Boolean).join(' ')
}


export default function CronDropdown() {
  const [selected, setSelected] = useState(crontabs[0])

  return (
      <>
        <div className="ml-10 mr-10 col-span-2">
          <DropdownMenu selected={selected} setSelected={setSelected} options={crontabs} >
            <Calendar className="flex-shrink-0 h-5 w-5 rounded-full" />
          </DropdownMenu>
        </div>
        <div className="col-span-2">
          <Crontab userInput={selected.value}/>
        </div>
      </>
  )
}


