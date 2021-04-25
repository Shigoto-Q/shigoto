import { useState } from 'react'
import axios from 'axios'

const IntervalSchedule = () => {
    const [option,setOption] = useState()
    const [input, setInput] = useState()
    const handleInput = (event: any) => {
        setInput(event.target.value)
    }
    const handleChange = (event: any) => {
        setOption(event.target.value)
    }
    const handleSubmit = (event: any) => {
        event.preventDefault()
        const data = {
            every: input,
            period: option
        }
        console.log(data)
        axios.post('/api/v1/schedule/interval/', data)
            .then(res => {})
            .catch(err => {})
    }
  return (
    <div className="ml-10 mb-5 mr-10 col-span-2">
    <form onSubmit={handleSubmit}>
      <label htmlFor="price" className="block text-sm font-medium text-gray-700">
        Every
      </label>
      <div className="mt-1 relative rounded-md shadow-sm">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <span className="text-gray-500 sm:text-sm">🕒</span>
        </div>
        <input
          type="number"
          name="input"
          id="price"
          className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-7 pr-12 sm:text-sm border-gray-300 rounded-md"
          placeholder="10"
          onChange={handleInput}
        />
        <div className="absolute inset-y-0 right-0 flex items-center">
          <label htmlFor="currency" className="sr-only">
            Period
          </label>
          <select
            id="currency"
            name="option"
            className="focus:ring-indigo-500 focus:border-indigo-500 h-full py-0 pl-2 pr-7 border-transparent bg-transparent text-gray-500 sm:text-sm rounded-md"
            onChange={handleChange}
          >
            <option value="days">Days</option>
            <option value="hours">Hours</option>
            <option value="minutes">Minutes</option>
            <option value="seconds">Seconds</option>
            <option value="microseconds">Microseconds</option>
          </select>
        </div>
      </div>
            <button type="submit" className="mt-2 bg-purple-400 hover:bg-blue-700 text-white font-bold py-2 px-10 rounded">
            Create interval
            </button>
    </form>
    </div>
  )
}

export default IntervalSchedule
