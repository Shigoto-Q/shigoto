import { Fragment, useState} from 'react'
import { Listbox, Transition } from '@headlessui/react'
import { Check, Menu, Sunrise } from 'react-feather'
import {connect} from "react-redux"
import {createSolar} from "../redux/actions/schedule/"

type SolarProps = {
  createSolar: any,
}
const people = [
  {
    id: 1,
    name: 'Astronomical dawn',
    value: 'dawn_astronomical'
  },
  {
    id: 2,
    name: 'Civil dawn',
    value: 'dawn_civil'
  },
  {
    id: 3,
    name: 'Nautical dawn',
    value: 'dawn_nautical'
  },
  {
    id: 4,
    name: 'Astronomical dusk',
    value: 'dusk_astronomical'
  },
  {
    id: 5,
    name: 'Civil dusk',
    value: 'dusk_civil'
  },
  {
    id: 6,
    name: 'Nautical dusk',
    value: 'dusk_nautical'
  },
  {
    id: 7,
    name: 'Solar noon',
    value: 'solar_noon'
  },
  {
    id: 8,
    name: 'Sunrise',
    value: 'sunrise'
  },
  {
    id: 9,
    name: 'Sunset',
    value: 'sunset'
  }
]

function classNames(...classes: any) {
  return classes.filter(Boolean).join(' ')
}

const SolarSchedule = ({createSolar}: SolarProps) => {
  const [selected, setSelected] = useState(people[0])
  const [latitude, setLatitude] = useState('')
  const [longtitude, setLongtitude] = useState('')

    const handleCreate = (event: any) => {
        event.preventDefault()
        createSolar(selected.value, latitude, longtitude)
    }
  return (
  <form onSubmit={e => handleCreate(e)}> 
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
      <label htmlFor="latitude" className="block text-sm font-medium text-gray-700">
        Latitude
      </label>
      <input
        type="text"
        name="latitude"
        id="latitude"
        autoComplete="latitude"
        placeholder="46.1512° N"
        className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
        onChange={e => setLatitude(e.target.value)}
      />
    </div>
    <div className="mt-5 sm:col-span-3">
      <label htmlFor="longtitude" className="block text-sm font-medium text-gray-700">
        Longtitude
      </label>
      <input
        type="text"
        name="longtitude"
        id="longtitude"
        autoComplete="longtitude"
        placeholder="14.9955° E"
        className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
        onChange={e => setLongtitude(e.target.value)}
      />
    </div>
    <button type="submit" className="mt-3 bg-purple-400 hover:bg-blue-700 text-white font-bold py-2 px-10 rounded">
    Create solar schedule
    </button>
    </div>
    </form>
  )
}

export default connect(null, {createSolar})(SolarSchedule)
