import ReactApexChart from "react-apexcharts";
import { MoreHorizontal } from "react-feather"
import { useState, useEffect } from "react"

interface TaskCardProps {
    label: string
    total: number
    Icon: any
    data: any
    cats: any
    oldTotal: any
}

function TaskCard({ label, total, Icon, data, cats, oldTotal }: TaskCardProps) {
    const [options, setOptions] = useState({
        chart: {
            id: 'realtime',
            animations: {
                enabled: true,
                dynamicAnimation: {
                    speed: 1000
                }
            },
            toolbar: {
                show: false
            },
            stroke: {
                curve: 'smooth'
            },
            markers: {
                size: 0
            },
            xaxis: {
                type: 'datetime',
                labels: {
                    format: 'YYYY',
                }
            },
            legend: {
                show: false
            },
        },
        xaxis: {
            categories: []
        },
    })

    const [series, setSeries] = useState([{}])
    useEffect(() => {
        setSeries(
            [
                {
                    name: "series-1",
                    data: data,
                }
            ]
        )
        setOptions(options => ({ ...options, xaxis: { categories: cats } }))
    }, [data, cats])
    return (
        <div className="flex flex-col bg-white shadow-lg rounded-sm  dark:text-gray-200 transition-colors duration-200 shadow-lg rounded-2xl p-4 bg-white dark:bg-gray-700 w-full">
            <div className="px-5 pt-5">
                <header className="flex justify-between items-start">
                </header>
                <h2 className="text-lg font-semibold text-gray-800 mb-2 dark:text-gray-200 transition-colors">{label}</h2>
                <div className="text-xs font-semibold text-gray-400 uppercase mb-1 dark:text-gray-400 transition-colors">Total</div>
                <div className="flex items-start">
                    <div className="text-3xl font-bold text-gray-800 mr-2 dark:text-gray-200 transition-colors">{total}</div>
                    <div className="text-sm font-semibold text-white px-1.5 bg-green-500 rounded-full">+{oldTotal}%</div>
                </div>
            </div>
            <div className="flex-grow">
                <ReactApexChart
                    options={options}
                    series={series}
                    type="line"
                    width={389} height={155}
                    className="-ml-8"
                />
            </div>
        </div>
    );
}

export default TaskCard
