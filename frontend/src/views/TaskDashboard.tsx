import { Component } from "react";
import TaskTable from "../components/tasks/TasksTable";
import TaskCard from "../components/tasks/TaskCard";
import { CheckCircle, XCircle, Loader } from "react-feather";
import { Drawer, ButtonToolbar, Button } from 'rsuite';
const token = localStorage.getItem("access");
const ws = new WebSocket(`ws://localhost:8080/status?token=${token}`);


type TaskStatus = {
    taskStatus: Object;
    options: any;
    data: any;
};

function getDate() {
    var currentdate = new Date();
    var datetime =
        currentdate.getHours() +
        ":" +
        currentdate.getMinutes() +
        ":" +
        currentdate.getSeconds();
    return datetime;
}

class Dashboard extends Component<TaskStatus, any> {
    _isMounted = false;
    constructor(props: any) {
        super(props);
        this.state = {
            taskStatus: Object,
            successData: [],
            failData: [],
            pendingData: [],
            time: [],
            oldSuccess: 0,
            oldFail: 0,
            oldPending: 0,
            show: false,
        };
        this.close = this.close.bind(this);
        this.toggleDrawer = this.toggleDrawer.bind(this);
    }
    close() {
        this.setState({ show: false });
    }

    toggleDrawer() {
        this.setState({ show: true });
    }

    componentWillMount() {
        this._isMounted = true;
        ws.onopen = () => {
            console.log("connected");
        };
        ws.onmessage = (message) => {
            if (this._isMounted) {
                this.setState({ taskStatus: JSON.parse(message.data)[0] });
                this.setState({
                    successData: [
                        ...this.state.successData,
                        JSON.parse(message.data)[0]["Success"],
                    ],
                });
                var frstLast = this.state.successData[
                    this.state.successData.length - 1
                ];
                var scnLast = this.state.successData[this.state.successData.length - 2];

                this.setState({
                    oldSuccess: (frstLast - scnLast) / 100,
                });

                this.setState({
                    failData: [
                        ...this.state.failData,
                        JSON.parse(message.data)[0]["Failure"],
                    ],
                });
                var fLast = this.state.failData[this.state.failData.length - 1];
                var f1Last = this.state.failData[this.state.failData.length - 2];

                this.setState({
                    oldFail: (fLast - f1Last) / 100,
                });
                this.setState({
                    pendingData: [
                        ...this.state.pendingData,
                        JSON.parse(message.data)[0]["Pending"],
                    ],
                });
                var pLast = this.state.pendingData[this.state.pendingData.length - 1];
                var p1Last = this.state.pendingData[this.state.pendingData.length - 2];

                this.setState({
                    oldPending: (pLast - p1Last) / 100,
                });
                this.setState({
                    time: [...this.state.time, getDate()],
                });
                if (this.state.time.length > 5) {
                    this.state.time.shift();
                }
                if (this.state.successData.length > 5) {
                    this.state.successData.shift();
                }
                if (this.state.failData.length > 5) {
                    this.state.failData.shift();
                }
            }
        };
        ws.onclose = () => {
            this._isMounted = false;
            console.log("disconnected");
        };
    }
    componentWillUnmount() {
        this._isMounted = false;
    }

    render() {
        return (
            <div>
                <div className="relative flex flex-col flex-1">
                    <main>
                        <div className="grid grid-cols-4 gap-4">
                            <div>
                                <ButtonToolbar>
                                    <Button onClick={this.toggleDrawer}>Open</Button>
                                </ButtonToolbar>
                                <Drawer
                                    show={this.state.show}
                                    onHide={this.close}
                                    backdropclassName="dark:text-gray-200 transition-colors duration-200  bg-white dark:bg-gray-700"
                                    dialogClassName="dark:text-gray-200 transition-colors duration-200  bg-white dark:bg-gray-700"

                                >
                                    <Drawer.Header
                                        className="dark:text-gray-200 transition-colors duration-200 dark:bg-gray-700 "
                                    >
                                        <Drawer.Title>Create a task</Drawer.Title>
                                    </Drawer.Header>
                                    <Drawer.Body
                                        className="dark:text-gray-200 transition-colors duration-200 dark:bg-gray-700 "

                                    >
                                    </Drawer.Body>
                                    <Drawer.Footer
                                        className="dark:text-gray-200 transition-colors duration-200  bg-white dark:bg-gray-700 "
                                    >
                                        <Button onClick={this.close} appearance="primary">Confirm</Button>
                                        <Button onClick={this.close} appearance="subtle">Cancel</Button>
                                    </Drawer.Footer>
                                </Drawer>
                            </div>
                            <TaskCard
                                cats={this.state.time}
                                label="Successful"
                                total={this.state.taskStatus["Success"]}
                                Icon={CheckCircle}
                                data={this.state.successData}
                                oldTotal={this.state.oldSuccess}
                            />
                            <TaskCard
                                cats={this.state.time}
                                label="Failed"
                                total={this.state.taskStatus["Failure"]}
                                Icon={XCircle}
                                data={this.state.failData}
                                oldTotal={this.state.oldFail}
                            />
                            <TaskCard
                                cats={this.state.time}
                                label="Pending"
                                total={this.state.taskStatus["Pending"]}
                                Icon={Loader}
                                data={this.state.pendingData}
                                oldTotal={this.state.oldPending}
                            />
                            <TaskTable />
                        </div>
                    </main>
                </div>
            </div>
        );
    }
}

export default Dashboard;
