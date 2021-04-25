import { Fragment, useState} from 'react'
import { Listbox, Transition } from '@headlessui/react'
import { Check, Menu, Sunrise } from 'react-feather'

const people = [
  {
    id: 1,
    name: 'Astronomical dawn',
    value: '10 * * * *'
  },
  {
    id: 2,
    name: 'Civil dawn',
    value: '* * * *'
  },
  {
    id: 3,
    name: 'Nautical dawn',
    value: '*/2 * * * *'
  },
  {
    id: 4,
    name: 'Astronomical dusk',
    value: '1-59/2 * * * *'
  },
  {
    id: 5,
    name: 'Civil dusk',
    value: '*/10 * * * *'
  },
  {
    id: 6,
    name: 'Nautical dusk',
    value: '*/6 * * * *'
  },
  {
    id: 7,
    name: 'Solar noon',
    value: '*/5 * * * * '
  },
  {
    id: 8,
    name: 'Sunrise',
    value: '0 0 * * FRI '
  },
  {
    id: 9,
    name: 'Sunset',
    value: '0 9-17 * * *'
  }
]

function classNames(...classes: any) {
  return classes.filter(Boolean).join(' ')
}

export default function SolarSchedule() {
  const [selected, setSelected] = useState(people[0])

  return (
  <form> 
    <div className="ml-10 mr-10 -mt-10 col-span-2">
    <Listbox value={selected} onChange={setSelected}>
      {({ open }) => (
        <>
          <Listbox.Label className="mt-10 mb-2 block text-sm font-medium text-gray-700">Select an event: </Listbox.Label>
          <div className="mt-1 relative">
            <Listbox.Button className="relative w-full bg-white border border-gray-300 rounded-md shadow-sm pl-3 pr-10 py-2 text-left cursor-default focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
              <span className="flex items-center">
                <Sunrise className="flex-shrink-0 h-5 w-5 rounded-full" />
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

    <div className="mt-10 sm:col-span-3">
      <label htmlFor="first_name" className="block text-sm font-medium text-gray-700">
        Latitude
      </label>
      <input
        type="text"
        name="first_name"
        id="first_name"
        autoComplete="given-name"
        placeholder="46.1512° N"
        className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
      />
    </div>
    <div className="mt-5 sm:col-span-3">
      <label htmlFor="last_name" className="block text-sm font-medium text-gray-700">
        Longtitude
      </label>
      <input
        type="text"
        name="last_name"
        id="last_name"
        autoComplete="family-name"
        placeholder="14.9955° E"
        className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
      />
    </div>
    <button type="submit" className="mt-3 bg-purple-400 hover:bg-blue-700 text-white font-bold py-2 px-10 rounded">
    Create solar schedule
    </button>
    </div>
    </form>
  )
}
 
