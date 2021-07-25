import React, { Fragment, useState } from 'react'
import {Listbox, Switch, Transition} from '@headlessui/react'
import { Check, Menu, Calendar } from 'react-feather'
import DropdownMenu from "../components/generic/DropdownMenu";
import {connect} from "react-redux";
import {checkAuthenticated, load_user} from "../redux/actions/auth";
import {createTask} from "../redux/actions/task";

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


type TaskProps = {
    isAuthenticated: boolean;
    user: any;
    createTask: any;
};





const TaskCreate = ({isAuthenticated, user, createTask} : TaskProps) => {
    let actualCrons:any = []
    const userCrons = JSON.parse(user || "{}").crontab;
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


    const handleClick = () => {
        setAtFirstStep(false)
    }




    const [selectedType, setSelectedType] = useState(taskTypes[0]);
    const [selectedCron, setSelectedCron] = useState(actualCrons[0]);
    const [atFirstStep, setAtFirstStep] = useState(true);
    const [oneoff, setOneoff] = useState(false);
    const [kwargs, setKwargs] = useState("");


    return (
        <div>
            {atFirstStep &&
            <div className="flex flex-col justify-center align-center">
                <div className="mt-10 w-2/4 self-center ">
                    <label
                        htmlFor="latitude"
                        className="block text-sm font-medium text-gray-700"
                    >
                        Task name
                    </label>
                    <input
                        type="text"
                        name="taskname"
                        id="taskname"
                        autoComplete="taskname"
                        className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    />
                </div>

                <div className="w-2/4 mt-5 self-center ">
                    <DropdownMenu selected={selectedType} setSelected={setSelectedType} options={taskTypes} label={"Select your task type:"} />
                </div>
                <div className = "flex flex-row justify-center align-center m-1.5">
                    <div className="w-2/5 mt-5 self-start">
                        <DropdownMenu selected={selectedCron} setSelected={setSelectedCron} options={actualCrons} label={"Select your crontab schedule:"} />
                    </div>
                    <div className="mt-10 ml-12">
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
                <div className="w-5/12 self-end justify-end ">
                    <div className="flex">
                        <button
                            onClick={handleClick}
                            className="mt-10 bg-purple-400 hover:bg-blue-700 text-white font-bold py-2 px-10 rounded self-center ml-36"
                        >
                            Next
                        </button>
                    </div>
                </div>


            </div>}
            {!atFirstStep && selectedType.id === 1 &&

            <div className="flex flex-col justify-center align-center">
                <div className="mt-10 w-2/4 self-center" >
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
                        className="mt-1 mb-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-700 dark:bg-gray-800  rounded-md"
                        onChange={(e) => setKwargs(e.target.value)}
                        required
                    />
                </div>
                <div className={"mt-10 w-2/4 self-center"}>
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
                        className="mt-1 mb-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm  dark:bg-gray-800 border-gray-700 rounded-md"
                    />
                </div>

            </div>

            }
        </div>
    )

}


const mapStateToProps = (state: any) => ({
    isAuthenticated: state.auth.isAuthenticated,
    user: state.auth.user,
});
export default connect(mapStateToProps, {
    checkAuthenticated,
    load_user,
    createTask,
})(TaskCreate);
