import { Component } from 'react'
import CronDropdown from "../components/crontab/CronSelect"
import IntervalSchedule from "../components/Interval"
import ClockedSchedule from "../components/ClockedSchedule"
import SolarSchedule from "../components/SolarSchedule"

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
        <div className="grid grid-cols-2 gap-4 divide-x-2 divide-opacity-50">  
            <div className="flex flex-wrap items-center">
                <p className="ml-20 py-12 font-serif text-gray-500 italic font-semibold text-lg subpixel-antialiased">
                    You can create your own crontab or select one of the premade schedules.
                </p>
            <div className="ml-10 mr-10 col-span-2">
                <CronDropdown/>
            </div>
        </div>
            <div className="flex items-center">
            <div className="">
                <p className="ml-20 -mt-4 py-12 font-serif text-gray-500 italic font-semibold text-lg subpixel-antialiased">
                Or, you can can create your own clock schedule, create an interval and even solar schedule!
                </p>
      <div className="hidden sm:block" aria-hidden="true">
        <div className="ml-10 -mt-5 py-5">
          <div className="border-t border-gray-200" />
        </div>
      </div>
                <IntervalSchedule/>
      <div className="hidden sm:block" aria-hidden="true">
        <div className="ml-10 py-5">
          <div className="border-t border-gray-200" />
        </div>
      </div>
                <ClockedSchedule/>
      <div className="hidden sm:block" aria-hidden="true">
        <div className="ml-10 py-5">
          <div className="border-t border-gray-200" />
        </div>
      </div>
                <SolarSchedule/>
            </div>
        </div>
            </div>
            )
    }
}
export default CronDash
