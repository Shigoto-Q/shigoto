import { useState } from "react";
import "flatpickr/dist/themes/material_green.css";

const Clocked = () => {
  //TODO install and parse with momentjs
  const [date, setDate] = useState(new Date().getDate());
  // eslint-disable-next-line
  const [time, setTime] = useState()
  return (
    <div className="ml-10 mr-10 mt-5 mb-5 col-span-2">
      <form>
        <label
          htmlFor="date"
          className="mb-2 block text-sm font-medium text-gray-700"
        >
          Select the exact date and time you want your task to run.
        </label>
        <input
          type="date"
          value={date}
          onChange={e => setDate(Date.parse(e.target.value))}
          className="mr-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border-gray-300 rounded-md"
        />
        <input
          type="time"
          value={time}
          className="focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border-gray-300 rounded-md"
        />
        <button
          type="submit"
          className="ml-2 bg-purple-400 hover:bg-blue-700 text-white font-bold py-2 px-10 rounded"
        >
          Create date & time schedule
        </button>
      </form>
    </div>
  );
};

export default Clocked;
