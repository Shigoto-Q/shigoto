import { createRef, useEffect, useState } from 'react'
import {isValidCron} from 'cron-validator'
import { useIsMount } from '../../custom_hooks/useIsMount'
import axios from 'axios'

import './Crontab.css'

type CronProps = {
    userInput: string
}

const Crontab = ({userInput}: CronProps) => {
    const [input, setInput] = useState(userInput)
    const [selectionStart, setSelectionStart] = useState(-1)
    const [pos, setPos] = useState(-1)
    const isMount = useIsMount()
    const [isValidMinute, setIsValidMinute] = useState(true)
    const [isValidHour, setIsValidHour] = useState(true)
    const [isValidMonthDay, setIsValidMonthDay] = useState(true)
    const [isValidMonth, setIsValidMonth] = useState(true)
    const [isValidWeekDay, setIsValidWeekDay] = useState(true)
    const inputRef = createRef<HTMLInputElement>()

    const handleCreate = () => {
        let crons = input.split(" ")
            const config = {
                minute: crons[0],
                hour: crons[1],
                day_of_month: crons[2],
                month_of_year: crons[3],
                day_of_week: crons[4]
            }
        // TODO show message
        axios.post('/api/v1/schedule/cron/', config)
            .then(res => {})
            .catch(err => {})
    }
    useEffect(() => {
        if(!isMount){
            setPos(checkActive())
        }
    }, [selectionStart])

    useEffect(() => {
        checkRegex()
    }, [input])

    useEffect(() => {
        setInput(userInput)
        }, [userInput])

    const selection = (position:any) => {

        const split = input.split(' ').filter(x => x !== '');
        var goal = split[position];

        var checkedEmpty = true;
        var checkedCnt = 0;
        for(var i = 0; i < input.length; i++) {
            if(input[i] !== ' ' && checkedEmpty) {
                checkedCnt++;
                checkedEmpty = false;
                if(checkedCnt === position+1) {
                    inputRef.current!.focus()
                    inputRef.current!.selectionStart = i
                    inputRef.current!.selectionEnd = i+goal.length;
                    setPos(position+1)
                }
            } else {
                checkedEmpty = true;
            }
        }
    }


    const checkActive = () => {
        var split = input.split(' ');
        var nextStart = -1
        var posCount = 0;
        for (var i = 0; i < split.length; i++) {
            if(split[i] !== ''){
                var indexOfSplit = input.indexOf(split[i], nextStart)
                nextStart = indexOfSplit + split[i].length
                if(selectionStart < indexOfSplit) {
                    return posCount;
                } else {
                    posCount++;
                }
            }
        }
        return posCount
    }

    const checkRegex = () => {
        const split = input.split(' ').filter(x => x !== '')
        setIsValidMinute(isValidCron(split[0] + ' * * * *'))
        setIsValidHour(isValidCron('* ' + split[1] + ' * * *'))
        setIsValidMonthDay(isValidCron('* * ' + split[2] + ' * *' ))
        setIsValidMonth(isValidCron('* * * ' + split[3]+ ' *' ))
        setIsValidWeekDay(isValidCron('* * * * ' + split[4]))
    }

    


    const handleInput = (event: any) => {
        setInput(event.target.value)
    }

    const handleFocus = (event: any) => {
        setSelectionStart(event.target.selectionStart)
    }   

    const handleKeyDown = (event: any) => {
        if(event.keyCode === 38) {
            setSelectionStart(event.target.value.length-1)
        } else if (event.keyCode === 40) {
            setSelectionStart(0)
        } else if(event.keyCode === 37 && selectionStart > 0) {
            setSelectionStart(event.target.selectionStart-1)
        } else if(event.keyCode === 39 && event.target.selectionStart < event.target.value.length) {
            setSelectionStart(event.target.selectionStart + 1)
        }
    }

    const switchValues = () => {
        switch(pos) {
            case 1:
                return "0-59"
            case 2:
                return "0-23"
            case 3:
                return "0-31"
            case 4:
                return "1-12"
            case 5:
                return "0-6"
            default: 
                return pos;
        }
    }


    return (
        <div className="cron-main bg-transparent">
            <p className="title-info">An easy way to plan your cron jobs.</p>
            <p className="title-sub-info">Plan your cron job here. Then, you can attach it to a task.</p>
            <input ref={inputRef} 
                id="input" 
                type="text" 
                value ={input} 
                onChange={handleInput} 
                onKeyDown = {handleKeyDown} 
                onClick={handleFocus} 
                className="text-purple-500 border-2 border-purple-300 focus:border-purple-800 text-opacity-90 bg-opacity-75 bg-gray"/>

            <div className = "info-parts">
                <p className = "cron-parts">
                    <span className = {!isValidMinute ? "part-wrong" : pos === 1 ? "cron-part-active" : "cron-part-inactive"}
                     onClick={() => selection(0)}>minute</span>
                    <span className = {!isValidHour ? "part-wrong" : pos === 2 ? "cron-part-active" : "cron-part-inactive"}
                    onClick={() => selection(1)}>hour</span>
                    <span className = {!isValidMonthDay ? "part-wrong" :  pos === 3 ? "cron-part-active" : "cron-part-inactive"}
                    onClick={() => selection(2)}>day(month)</span>
                    <span className = {!isValidMonth? "part-wrong" :  pos === 4 ? "cron-part-active" : "cron-part-inactive"}
                    onClick={() => selection(3)}>month</span>
                    <span className = {!isValidWeekDay? "part-wrong" :  pos === 5 ? "cron-part-active" : "cron-part-inactive"}
                    onClick={() => selection(4)}>day(week)</span>
                </p>
            </div>
            <table className="options-table">
            <tbody>
            <tr>
                <td style={{textAlign: "center"}} >*</td>
                <td>any value</td>
              </tr>
              <tr>
                <td style={{textAlign: "center"}}>,</td>
                <td>list separator</td>
              </tr>
              <tr>
                <td style={{textAlign: "center"}}>-</td>
                <td>range of values</td>
              </tr>
              <tr>
                <td style={{textAlign: "center"}} >/</td>
                <td>step values</td>
              </tr>
              {pos !== -1  &&
              <tr>
                <td style={{textAlign: "center"}}>{switchValues()}</td>
                <td>allowed values</td>
              </tr>
              }
              {pos === 4  &&
              <tr>
                <td style={{textAlign: "center"}}>JAN-DEC</td>
                <td>alternative values</td>
              </tr>
              }
              {pos === 5  &&
              <tr>
                <td style={{textAlign: "center"}}>SUN-SAT</td>
                <td>alternative single values</td>
              </tr>
              }
             {pos === 5  &&
              <tr>
                <td style={{textAlign: "center"}}>7</td>
                <td>sunday (non-standard)</td>
              </tr>
              }
            </tbody>

            </table>
        <div className="mt-5">
            <button className="mr-2 bg-purple-400 hover:bg-blue-700 text-white font-bold py-2 px-10 rounded">
            Attach to task
            </button>
            <button onClick={handleCreate} className="ml-2 bg-purple-400 hover:bg-blue-700 text-white font-bold py-2 px-10 rounded">
            Create crontab
            </button>
            </div>
        </div>
    )
}

export default Crontab 
