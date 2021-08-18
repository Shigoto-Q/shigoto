import { Fragment, useState } from "react";
import { Listbox, Transition } from "@headlessui/react";
import { Check, Menu, Sunrise } from "react-feather";
import { connect } from "react-redux";
import { createSolar } from "../redux/actions/schedule/";
import DropdownMenu from "./generic/DropdownMenu";

type SolarProps = {
  createSolar: any;
};
const solar = [
  {
    id: 1,
    name: "Astronomical dawn",
    value: "dawn_astronomical",
  },
  {
    id: 2,
    name: "Civil dawn",
    value: "dawn_civil",
  },
  {
    id: 3,
    name: "Nautical dawn",
    value: "dawn_nautical",
  },
  {
    id: 4,
    name: "Astronomical dusk",
    value: "dusk_astronomical",
  },
  {
    id: 5,
    name: "Civil dusk",
    value: "dusk_civil",
  },
  {
    id: 6,
    name: "Nautical dusk",
    value: "dusk_nautical",
  },
  {
    id: 7,
    name: "Solar noon",
    value: "solar_noon",
  },
  {
    id: 8,
    name: "Sunrise",
    value: "sunrise",
  },
  {
    id: 9,
    name: "Sunset",
    value: "sunset",
  },
];

function classNames(...classes: any) {
  return classes.filter(Boolean).join(" ");
}

const SolarSchedule = ({ createSolar }: SolarProps) => {
  const [selected, setSelected] = useState(solar[0]);
  const [latitude, setLatitude] = useState("");
  const [longtitude, setLongtitude] = useState("");

  const handleCreate = (event: any) => {
    event.preventDefault();
    createSolar(selected.value, latitude, longtitude);
  };
  return (
    <form onSubmit={(e) => handleCreate(e)}>
      <div className="ml-10 mr-10 -mt-10 col-span-2">
        <DropdownMenu selected={selected} setSelected={setSelected} options={solar}>
          <Sunrise className="flex-shrink-0 h-5 w-5 rounded-full" />
        </DropdownMenu>

        <div className="mt-10 sm:col-span-3">
          <label
            htmlFor="latitude"
            className="block text-sm font-medium text-gray-700"
          >
            Latitude
          </label>
          <input
            type="text"
            name="latitude"
            id="latitude"
            autoComplete="latitude"
            placeholder="46.1512° N"
            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
            onChange={(e) => setLatitude(e.target.value)}
          />
        </div>
        <div className="mt-5 sm:col-span-3">
          <label
            htmlFor="longtitude"
            className="block text-sm font-medium text-gray-700"
          >
            Longtitude
          </label>
          <input
            type="text"
            name="longtitude"
            id="longtitude"
            autoComplete="longtitude"
            placeholder="14.9955° E"
            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
            onChange={(e) => setLongtitude(e.target.value)}
          />
        </div>
        <button
          type="submit"
          className="mt-3 bg-purple-400 hover:bg-blue-700 text-white font-bold py-2 px-10 rounded"
        >
          Create solar schedule
        </button>
      </div>
    </form>
  );
};

export default connect(null, { createSolar })(SolarSchedule);
