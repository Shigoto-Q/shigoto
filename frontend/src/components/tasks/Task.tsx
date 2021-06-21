import { Switch } from "@headlessui/react";
import { connect } from "react-redux";
import { checkAuthenticated, load_user } from "../../redux/actions/auth/";
import { createTask } from "../../redux/actions/task/";
import { Fragment, useState } from "react";
import { Listbox, Transition } from "@headlessui/react";
import { Check, Menu, } from "react-feather";
import SpinnerComponent from "../Spinner";

type TaskProps = {
  isAuthenticated: boolean;
  user: any;
  createTask: any;
};
function classNames(...classes: any) {
  return classes.filter(Boolean).join(" ");
}

const CreateTask = ({ isAuthenticated, user, createTask }: TaskProps) => {
  const [enabled, setEnabled] = useState(true);
  const [oneoff, setOneoff] = useState(false);
  const [crontab, setCrontab] = useState({ value: "1 * * *", id: 1 });
  const [kwargs, setKwargs] = useState("");
  const [taskName, setTaskName] = useState("");
  const userCrons = JSON.parse(user || "{}").crontab;
  let actualCrons:any = []
  if(userCrons) {
      actualCrons = userCrons.map((item: any) => {
      return {
        value: [
          item.minute,
          item.hour,
          item.day_of_month,
          item.month_of_year,
        ].join(" "),
        id: item.id,
      };
    });
  }

  const handleSubmit = (event: any) => {
    event.preventDefault();
    createTask(taskName, crontab.id, kwargs, oneoff, enabled);
  };

  return (
    <div className="flex flex-col bg-white rounded-sm shadow-lg rounded-2xl p-4 bg-white dark:bg-gray-700 w-full">
      <header className="flex justify-between items-start mb-2"></header>
      <h2 className="text-md font-semibold text-gray-800 mb-2 ml-2 dark:text-white">
        Create a task
      </h2>
      <div className="flex flex-nowrap">
        <form onSubmit={(e) => handleSubmit(e)}>
          <div className="ml-2 mb-2">
            <label
              htmlFor="task"
              className="block text-sm font-medium text-gray-700 dark:text-white"
            >
              Task name:
            </label>
            <input
              type="text"
              name="task"
              id="task"
              placeholder="My first task"
              className="bg-gray-100 dark:bg-gray-800 mt-1 mb-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-700 rounded-md"
              onChange={(e) => setTaskName(e.target.value)}
              required
            />
            <label
              htmlFor="kwargs"
              className=" dark:text-white block text-sm font-medium text-gray-700"
            >
              Request endpoint:
            </label>
            <input
              type="text"
              name="kwargs"
              id="kwargs"
              placeholder="https://www.google.com"
              className="mt-1 mb-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-700 bg-gray-100 dark:bg-gray-800  rounded-md"
              onChange={(e) => setKwargs(e.target.value)}
              required
            />
            <label
              htmlFor="exp"
              className=" dark:text-white block text-sm font-medium text-gray-700"
            >
              Expire timedelta with seconds:
            </label>
            <input
              type="text"
              name="exp"
              id="exp"
              placeholder="100"
              className="mt-1 mb-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm bg-gray-100 dark:bg-gray-800 border-gray-700 rounded-md"
            />
            <button
              type="submit"
              className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-purple-400 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
            >
              Submit
            </button>
          </div>
        </form>
        <div className="ml-2">
          <label
            htmlFor="kwargs"
            className="block text-sm font-medium text-gray-700 dark:text-white"
          >
            Select a crontab
          </label>
          <div className="col-span-2">
            <Listbox value={crontab} onChange={setCrontab}>
              {({ open }) => (
                <>
                  <div className="mt-1 relative">
                    <Listbox.Button className="relative w-full bg-white dark:bg-gray-800 rounded-md shadow-sm pl-3 pr-10 py-2 text-left cursor-default focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                      <span className="flex justify-center">
                        <span className="ml-3  dark:text-gray-200 ">
                          {crontab.value}
                        </span>
                      </span>
                      <span className="ml-3 absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                        <Menu
                          className="h-5 w-5 text-gray-400"
                          aria-hidden="true"
                        />
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
                        className="absolute mt-1 w-full bg-white dark:bg-gray-800 shadow-lg max-h-56 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm"
                      >
                        {actualCrons.map((person: any) => (
                          <Listbox.Option
                            key={person.id}
                            className={({ active }) =>
                              classNames(
                                active
                                  ? "text-white bg-indigo-600"
                                  : "text-gray-900",
                                "cursor-default select-none dark:text-gray-200 elative py-2 pl-3 pr-9"
                              )
                            }
                            value={person}
                          >
                            {({ selected, active }) => (
                              <>
                                <div className="flex items-center">
                                  <span
                                    className={classNames(
                                      selected
                                        ? "font-semibold"
                                        : "font-normal",
                                      "ml-3 block truncate"
                                    )}
                                  >
                                    {person.value}
                                  </span>
                                </div>

                                {selected ? (
                                  <span
                                    className={classNames(
                                      active ? "text-white" : "text-indigo-600",
                                      "absolute inset-y-0 right-0 flex items-center pr-4"
                                    )}
                                  >
                                    <Check
                                      className="h-5 w-5"
                                      aria-hidden="true"
                                    />
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
          <div className="mt-8">
            <Switch.Group>
              <Switch.Label className="mr-4 dark:text-white">
                Enabled
              </Switch.Label>
              <Switch
                checked={enabled}
                onChange={setEnabled}
                className={`${
                  enabled ? "bg-purple-400" : "bg-gray-500"
                }  inline-flex items-center h-6 rounded-full w-11 transition-colors focus:outline-none`}
              >
                <span
                  className={`${
                    enabled ? "translate-x-6" : "translate-x-1"
                  } inline-block w-4 h-4 transform bg-white rounded-full transition-transform`}
                />
              </Switch>
            </Switch.Group>
          </div>
          <div className="mt-10">
            <Switch.Group>
              <Switch.Label className="mr-4 dark:text-white">
                One-off
              </Switch.Label>
              <Switch
                checked={oneoff}
                onChange={setOneoff}
                className={`${
                  oneoff ? "bg-purple-400" : "bg-gray-500"
                }  inline-flex items-center h-6 rounded-full w-11 transition-colors focus:outline-none`}
              >
                <span
                  className={`${
                    oneoff ? "translate-x-6" : "translate-x-1"
                  } inline-block w-4 h-4 transform bg-white rounded-full transition-transform`}
                />
              </Switch>
            </Switch.Group>
          </div>
        </div>
      </div>
    </div>
  );
};

const mapStateToProps = (state: any) => ({
  isAuthenticated: state.auth.isAuthenticated,
  user: state.auth.user,
});
export default connect(mapStateToProps, {
  checkAuthenticated,
  load_user,
  createTask,
})(CreateTask);
