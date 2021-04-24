/* This example requires Tailwind CSS v2.0+ */
import { Fragment, useState } from 'react'
import { Listbox, Transition } from '@headlessui/react'
import { Check, Menu, Calendar } from 'react-feather'

const people = [
  {
    id: 1,
    name: '10 * * * * - At minute 10'
  },
  {
    id: 2,
    name: '* * * * * - Every minute',
  },
  {
    id: 3,
    name: '*/2 * * * * - At every 2nd minute',
  },
  {
    id: 4,
    name: '1-59/2 * * * * - At every 2nd minute from 1 through 59',
  },
  {
    id: 5,
    name: '*/10 * * * * - At every 10th minute',
  },
  {
    id: 6,
    name: '*/6 * * * * - At every 6th minute',
  },
  {
    id: 7,
    name: '*/5 * * * * - At every 5th minute',
  },
  {
    id: 8,
    name: '0 0 * * FRI - At 00:00 on Friday',
  },
  {
    id: 9,
    name: '0 9-17 * * * - At minute 0 past every hour from 9 through 17',
  },
  {
    id: 10,
    name: '0 0 * * - 1-5 At 00:00 every day-of-week from Monday through Friday',
  },
]

function classNames(...classes: any) {
  return classes.filter(Boolean).join(' ')
}

export default function CronDropdown() {
  const [selected, setSelected] = useState(people[3])

  return (
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
  )
}
 
