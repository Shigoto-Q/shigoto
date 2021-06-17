import { Fragment } from 'react'
import { Menu, Transition } from '@headlessui/react'
import { User } from 'react-feather'
import { Link } from "react-router-dom"
import { logout } from "../redux/actions/auth"
import { connect } from "react-redux"

function classNames(...classes: any) {
    return classes.filter(Boolean).join(' ')
}

type DropDownProps = {
    logout: any
    user: string
}
const UserDropDown = ({ logout, user}: DropDownProps) => {
    return (
        <Menu as="div" className="relative inline-flex dark:text-gray-300">
            {({ open }) => (
                <>
                    <div>
                        <Menu.Button className="inline-flex justify-center items-center group">
                            <User className="" aria-hidden="true" />
                            <div className="flex items-center truncate">
                                <span className="truncate ml-2 text-sm font-medium group-hover:text-gray-800">{user}</span>
                                <svg className="w-3 h-3 flex-shrink-0 ml-1 fill-current text-gray-400" viewBox="0 0 12 12">
                                    <path d="M5.9 11.4L.5 6l1.4-1.4 4 4 4-4L11.3 6z" />
                                </svg>
                            </div>

                        </Menu.Button>
                    </div>

                    <Transition
                        show={open}
                        as={Fragment}
                        enter="transition ease-out duration-100"
                        enterFrom="transform opacity-0 scale-95"
                        enterTo="transform opacity-100 scale-100"
                        leave="transition ease-in duration-75"
                        leaveFrom="transform opacity-100 scale-100"
                        leaveTo="transform opacity-0 scale-95"
                    >
                        <Menu.Items
                            static
                            className="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
                        >
                            <div className="py-1">
                                <Menu.Item>
                                    {({ active }) => (
                                        <Link
                                            to="/dashboard/profile-settings"
                                            className={classNames(
                                                active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                                                'block px-4 py-2 text-sm'
                                            )}
                                        >
                                            Account settings
                                        </Link>
                                    )}
                                </Menu.Item>
                                <Menu.Item>
                                    {({ active }) => (
                                        <Link
                                            to="/"
                                            className={classNames(
                                                active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                                                'block w-full text-left px-4 py-2 text-sm'
                                            )}
                                            onClick={logout}
                                        >
                                            Sign out
                                        </Link>
                                    )}
                                </Menu.Item>
                            </div>
                        </Menu.Items>
                    </Transition>
                </>
            )}
        </Menu>
    )
}


export default connect(null, { logout })(UserDropDown);
