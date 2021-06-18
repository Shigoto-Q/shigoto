import { Fragment, useState } from 'react'
import { Listbox, Transition } from '@headlessui/react'
import { Check, Menu, Calendar } from 'react-feather'
import Crontab from "../crontab/Crontab"

const people = [
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
  const [selected, setSelected] = useState(people[0])

  return (
  <>
    <div className="ml-10 mr-10 col-span-2">
    <Listbox value={selected} onChange={setSelected}>
      {({ open }) => (
        <>
          <Listbox.Label className="block text-sm font-medium text-gray-700">Example crontabs: </Listbox.Label>
          <div className="mt-1 relative">
            <Listbox.Button className="relative w-full bg-white border border-gray-300 rounded-md shadow-sm pl-3 pr-10 py-2 text-left cursor-default focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
              <span className="flex items-center">
                <Calendar className="flex-shrink-0 h-5 w-5 rounded-full" />
                <span className="ml-3 block">{selected.name}</span>
              </span>
              <span className="ml-3 absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                <Menu className="h-5 w-5 text-gray-400" aria-hidden="true" />
              </span>
            </Listbox.Button>

            <Transition
              show={open}
              as={Fragment}
              leave="transition ease-in duration-100"
              leaveFrom="opacity-100"
              leaveTo="opacity-0"
            >
              <Listbox.Options
                static
                className="absolute mt-1 w-full bg-white shadow-lg max-h-56 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm"
              >
                {people.map((person) => (
                 <Listbox.Option
                    key={person.id}
                    className={({ active }) =>
                      classNames(
                        active ? 'text-white bg-indigo-600' : 'text-gray-900',
                        'cursor-default select-none relative py-2 pl-3 pr-9'
                      )
                    }
                    value={person}
                  >
                    {({ selected, active }) => (
                      <>
                        <div className="flex items-center">
                          <span
                            className={classNames(selected ? 'font-semibold' : 'font-normal', 'ml-3 block truncate')}
                          >
                            {person.name}
                          </span>
                        </div>

                        {selected ? (
                          <span
                            className={classNames(
                              active ? 'text-white' : 'text-indigo-600',
                              'absolute inset-y-0 right-0 flex items-center pr-4'
                            )}
                          >
                            <Check className="h-5 w-5" aria-hidden="true" />
                          </span>
                        ) : null}
                      </>
                    )}
                  </Listbox.Option>
                ))}
              </Listbox.Options>
            </Transition>
          </div>
        </>
      )}
    </Listbox>
    </div>
            <div className="col-span-2">
                <Crontab userInput={selected.value}/>
            </div>
    </>
  )
}
