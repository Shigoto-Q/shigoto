import { Component } from "react"
import {Steps, Panel, ButtonGroup, Button } from "rsuite"
import 'rsuite/dist/styles/rsuite-default.css';

interface TaskState {
    step: number
}

class TaskCreate extends Component<TaskState, any> {
    constructor(props: any) {
        super(props)
        this.state = {
            step: 0
        };

        this.onChange = this.onChange.bind(this)
        this.onNext = this.onNext.bind(this)
        this.onPrevious = this.onPrevious.bind(this)
    }

    onChange = (nextStep: number) => {
        this.setState({ step: nextStep < 0 ? 0 : nextStep > 3 ? 3 : nextStep })
    }

    onNext = () => {
        this.setState({ step: this.state.step + 1 })
    }
    onPrevious = () => {
        this.setState({ step: this.state.step - 1 })
    }

    render() {
        return (
            <div>
                <Steps current={this.state.step}>
                    <Steps.Item className="!dark:text-gray-200" title="Finished" description="Description" />
                    <Steps.Item title="In Progress" description="Description" />
                    <Steps.Item title="Waiting" description="Description" />
                    <Steps.Item title="Waiting" description="Description" />
                </Steps>
                <hr />
                <Panel className="dark:text-gray-200" header={`Step: ${this.state.step + 1}`}>
                </Panel>
                <hr />
                <ButtonGroup>
                    <Button onClick={this.onPrevious} disabled={this.state.step === 0}>
                        Previous
        </Button>
                    <Button onClick={this.onNext} disabled={this.state.step === 3}>
                        Next
        </Button>
                </ButtonGroup>
            </div>
        );
    }
}


export default TaskCreate
