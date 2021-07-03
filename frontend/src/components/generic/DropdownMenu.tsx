import {Listbox, Transition} from "@headlessui/react";
import {Calendar, Check, Icon, Menu} from "react-feather";
import React, {Fragment} from "react";

type DropdownMenuProps = {
    selected: { id:number, name:string, value: string },
    setSelected:  React.Dispatch<React.SetStateAction<{id: number, name:string, value: string}>>,
    options: Array<{ id:number,name:string, value:string }>
    children?: any
}

function classNames(...classes: any) {
    return classes.filter(Boolean).join(' ')
}

const DropdownMenu = (props:DropdownMenuProps) => {
    return (
        <>
            <Listbox value={props.selected} onChange={props.setSelected}>
                {({ open }) => (
                    <>
                        <Listbox.Label className="block text-sm font-medium text-gray-700">Select your task type: </Listbox.Label>
                        <div className="mt-1 relative">
                            <Listbox.Button className="relative w-full bg-white border border-gray-300 rounded-md shadow-sm pl-3 pr-10 py-2 text-left cursor-default focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"><span className="flex items-center">
                                {props.children}
                                <span className="ml-3 block">{props.selected.name}</span>
                            </span>
                                <span className="ml-3 absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none"><Menu className="h-5 w-5 text-gray-400" aria-hidden="true" /></span>
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
                                    {props.options.map((option) => (
                                        <Listbox.Option
                                            key={option.id}
                                            className={({ active }) =>
                                                classNames(
                                                    active ? 'text-white bg-indigo-600' : 'text-gray-900',
                                                    'cursor-default select-none relative py-2 pl-3 pr-9'
                                                )
                                            }
                                            value={option}
                                        >
                                            {({ selected, active }) => (
                                                <>
                                                    <div className="flex items-center">
                                                        <span
                                                            className={classNames(selected ? 'font-semibold' : 'font-normal', 'ml-3 block truncate')}
                                                        >{option.name}
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
                                                    ) : null}</>
                                            )}
                                        </Listbox.Option>
                                    ))}
                                </Listbox.Options>
                            </Transition>
                        </div>
                    </>
                )}
            </Listbox>
        </>
    )
}



export default DropdownMenu
