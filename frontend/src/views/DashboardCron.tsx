import { Component } from 'react'
import Crontab from "../components/crontab/Crontab"
import axios from 'axios'


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
        axios.get('/api/v1/cron/')
            .then(res => {
                this.setState({crons: res.data})
            })
            .catch(err => {})
    }
    render() {
        return (
        <>
            <p className="py-12 font-serif text-purple-500 italic font-semibold text-lg subpixel-antialiased place-self-center">
                You can create your own crontab or select one of the premade schedules.
            </p>
        <div className="grid grid-cols-2 gap-2 divide-x-2 divide-purple-300 divide-opacity-50">  
            <div className="-ml-10">
                <Crontab/>
            </div>
        <div className="grid grid-cols-3">
            <div>
            </div>
            <p className="py-12 font-serif text-purple-500 italic font-semibold text-lg subpixel-antialiased place-self-center">
                Premade crontabs:
            </p>
            <div>
            </div>
                <ul className="ml-14 list-disc">
                  <li><a href="every-minute">every minute</a></li>
                  <li><a href="every-1-minute">every 1 minute</a></li>
                  <li><a href="every-2-minutes">every 2 minutes</a></li>
                  <li><a href="every-even-minute">every even minute</a></li>
                  <li><a href="every-uneven-minute">every uneven minute</a></li>
                  <li><a href="every-3-minutes">every 3 minutes</a></li>
                  <li><a href="every-4-minutes">every 4 minutes</a></li>
                  <li><a href="every-5-minutes">every 5 minutes</a></li>
                  <li><a href="every-five-minutes">every five minutes</a></li>
                  <li><a href="every-6-minutes">every 6 minutes</a></li>
                  <li><a href="every-10-minutes">every 10 minutes</a></li>
                  <li><a href="every-15-minutes">every 15 minutes</a></li>
                  <li><a href="every-fifteen-minutes">every fifteen minutes</a></li>
                  <li><a href="every-ten-minutes">every ten minutes</a></li>
                  <li><a href="every-quarter-hour">every quarter hour</a></li>
                  <li><a href="every-20-minutes">every 20 minutes</a></li>
                  <li><a href="every-30-minutes">every 30 minutes</a></li>
                </ul>
                <ul className="mr-14 list-disc">
                  <li><a href="every-minute">every minute</a></li>
                  <li><a href="every-1-minute">every 1 minute</a></li>
                  <li><a href="every-2-minutes">every 2 minutes</a></li>
                  <li><a href="every-even-minute">every even minute</a></li>
                  <li><a href="every-uneven-minute">every uneven minute</a></li>
                  <li><a href="every-3-minutes">every 3 minutes</a></li>
                  <li><a href="every-4-minutes">every 4 minutes</a></li>
                  <li><a href="every-5-minutes">every 5 minutes</a></li>
                  <li><a href="every-five-minutes">every five minutes</a></li>
                  <li><a href="every-6-minutes">every 6 minutes</a></li>
                  <li><a href="every-10-minutes">every 10 minutes</a></li>
                  <li><a href="every-15-minutes">every 15 minutes</a></li>
                  <li><a href="every-fifteen-minutes">every fifteen minutes</a></li>
                  <li><a href="every-ten-minutes">every ten minutes</a></li>
                  <li><a href="every-quarter-hour">every quarter hour</a></li>
                  <li><a href="every-20-minutes">every 20 minutes</a></li>
                  <li><a href="every-30-minutes">every 30 minutes</a></li>
                </ul>
                <ul className="mr-14 list-disc">
                  <li><a href="every-minute">every minute</a></li>
                  <li><a href="every-1-minute">every 1 minute</a></li>
                  <li><a href="every-2-minutes">every 2 minutes</a></li>
                  <li><a href="every-even-minute">every even minute</a></li>
                  <li><a href="every-uneven-minute">every uneven minute</a></li>
                  <li><a href="every-3-minutes">every 3 minutes</a></li>
                  <li><a href="every-4-minutes">every 4 minutes</a></li>
                  <li><a href="every-5-minutes">every 5 minutes</a></li>
                  <li><a href="every-five-minutes">every five minutes</a></li>
                  <li><a href="every-6-minutes">every 6 minutes</a></li>
                  <li><a href="every-10-minutes">every 10 minutes</a></li>
                  <li><a href="every-15-minutes">every 15 minutes</a></li>
                  <li><a href="every-fifteen-minutes">every fifteen minutes</a></li>
                  <li><a href="every-ten-minutes">every ten minutes</a></li>
                  <li><a href="every-quarter-hour">every quarter hour</a></li>
                  <li><a href="every-20-minutes">every 20 minutes</a></li>
                  <li><a href="every-30-minutes">every 30 minutes</a></li>
                </ul>
                </div>
        </div>
            </>
            )
    }
}
export default CronDash
