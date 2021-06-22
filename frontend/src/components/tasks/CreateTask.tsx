import { Component } from "react";

class CreateTask extends Component<any, any> {
    _isMounted = false;
    constructor(props: any) {
        super(props);
        this.state = {
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

    render() {
        return (
            <div className="flex">
                <button onClick={this.toggleDrawer}> Create a task </button>
                <div className="flex items-center justify-center ">
                </div>
            </div>
        );
    }
}

export default CreateTask
