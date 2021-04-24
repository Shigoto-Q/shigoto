import { Component } from 'react'
import Crontab from "../components/crontab/Crontab"
import CronDropdown from "../components/crontab/CronSelect"


type CronState = {
    crons: Array<Object>
}
class CronDash extends Component<CronState, any> {
    constructor(props: any) {
        super(props)
            this.state = {
            crons: {}
            }
    }
    componentDidMount() {
    }
    render() {
        return (
        <>
            <p className="py-12 font-serif text-purple-500 italic font-semibold text-lg subpixel-antialiased place-self-center">
                You can create your own crontab or select one of the premade schedules.
            </p>
        <div className="grid grid-cols-2 gap-4 divide-x-2 divide-opacity-50">  
            <div className="ml-10">
            <div className="ml-10 mr-10 col-span-2">
                <CronDropdown/>
            </div>
            <div className="col-span-2">
                <Crontab/>
            </div>
            </div>
            <div className="ml-10 mr-10">
            </div>
        </div>
            </>
            )
    }
}
export default CronDash
