import Flatpickr from "react-flatpickr";
import { useState } from "react"
import "flatpickr/dist/themes/material_green.css";

const Clocked = () => {
    const [date, setDate] = useState(new Date())    
    return (
    <div className="ml-10 mr-10 mt-5 mb-5 col-span-2">
        <form>
            <label htmlFor="date" className="mb-2 block text-sm font-medium text-gray-700">
                Select the exact date and time you want your task to run.
            </label>
            <Flatpickr
                data-enable-time
                value={date}
                onChange={date => setDate}
              />
            <button type="submit" className="ml-2 bg-purple-400 hover:bg-blue-700 text-white font-bold py-2 px-10 rounded">
            Create date & time schedule
            </button>
          </form>
    </div>
    )
}


export default Clocked
