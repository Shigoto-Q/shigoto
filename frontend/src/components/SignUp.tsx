import { Component } from 'react'
import axios from 'axios'
import { toast } from "react-toastify"
import 'react-toastify/dist/ReactToastify.css'
import { motion } from 'framer-motion'
import pageTranstion from "../layout/transitions"

toast.configure()
type Props = {
    username: string
    first_name: string,
    last_name: string,
    email: string,
    country: string,
    password: string,
    re_passowrd: string,
    street_address: string,
    company: string,
    city: string,
    zip: number,
    state?: string
}

class SignUp extends Component<Props, any> { 
    constructor(props: any) {
        super(props)
            this.state = {
            username: "",
            first_name: "",
            last_name: "",
            email: "",
            country: "",
            password: "",
            re_passowrd: "",
            street_address: "",
            company: "",
            city: "",
            zip: "",
            state: ""
            }
        this.handleSubmit = this.handleSubmit.bind(this)
        this.handleChange = this.handleChange.bind(this)
    }
    handleChange = (event: any) => {
        const value = event.target.value
            this.setState({
                ...this.state,
                [event.target.name]: value
                    })
    }
    handleSubmit = (event: any) => {
        event.preventDefault()
            const body = {
                username: this.state.username,
                first_name: this.state.first_name,
                last_name: this.state.last_name,
                email: this.state.email,
                country: this.state.country,
                password: this.state.password,
                street_address: this.state.street_address,
                company: this.state.company,
                city: this.state.city,
                zip: this.state.zip,
                state: this.state.state
            } 
            axios.post("/auth/users/", body)
                .then(res => {
                    console.log(res)
                        })
            .catch(err => {
                // TODO create custom notification component
                toast("somethings wrong!", 
                        {
                        position: "bottom-center",
                        autoClose: 5000,
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: true,
                        draggable: false,
                        progress: undefined,
                        })
            })
        }
    render () {
        return (
        <motion.div initial="out" animate="in" exit="out" variants={pageTranstion} className="flex justify-center">
         <div className="hidden sm:block" aria-hidden="true">
            <div className="py-5">
              <div className="border-t border-gray-200" />
            </div>
          </div>

          <div className="mt-10 sm:mt-0">
            <div className="md:grid md:grid-cols-3 md:gap-6">
              <div className="md:col-span-1">
                <div className="px-4 sm:px-0">
                  <h3 className="text-lg font-medium leading-6 text-gray-900">Personal Information</h3>
                  <p className="mt-1 text-sm text-gray-600">Use a permanent address where you can receive mail.</p>
                </div>
              </div>
              <div className="mt-5 md:mt-0 md:col-span-2">
                <form onSubmit={this.handleSubmit}>
                  <div className="shadow overflow-hidden sm:rounded-md">
                    <div className="px-4 py-5 bg-white sm:p-6">
                      <div className="grid grid-cols-6 gap-6">
                        <div className="col-span-6 sm:col-span-3">
                          <label htmlFor="first_name" className="block text-sm font-medium text-gray-700">
                            First name
                          </label>
                          <input
                            type="text"
                            name="first_name"
                            id="first_name"
                            autoComplete="given-name"
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                            required
                            onChange={this.handleChange}
                          />
                        </div>

                        <div className="col-span-6 sm:col-span-3">
                          <label htmlFor="last_name" className="block text-sm font-medium text-gray-700">
                            Last name
                          </label>
                          <input
                            type="text"
                            name="last_name"
                            id="last_name"
                            autoComplete="family-name"
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                            onChange={this.handleChange}
                            required
                          />
                        </div>
                        <div className="col-span-6 sm:col-span-3">
                          <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                            E-mail address
                          </label>
                          <input
                            type="text"
                            name="email_address"
                            id="email_address"
                            autoComplete="email"
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                            required
                            onChange={this.handleChange}
                          />
                        </div>

                        <div className="col-span-6 sm:col-span-3">
                          <label htmlFor="username" className="block text-sm font-medium text-gray-700">
                            Username
                          </label>
                          <input
                            type="text"
                            name="username"
                            id="username"
                            autoComplete="username"
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                            required
                            onChange={this.handleChange}
                          />
                        </div>
                        <div className="col-span-6 sm:col-span-3">
                          <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                            Password
                          </label>
                          <input
                            type="password"
                            name="password"
                            id="password"
                            autoComplete="password"
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                            required
                            onChange={this.handleChange}
                          />
                        </div>
                        <div className="col-span-6 sm:col-span-3">
                          <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                            Confirm password
                          </label>
                          <input
                            type="password"
                            name="re_password"
                            id="re_password"
                            autoComplete="password"
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                            required
                            onChange={this.handleChange}
                          />
                        </div>
                        <div className="col-span-6 sm:col-span-3">
                          <label htmlFor="country" className="block text-sm font-medium text-gray-700">
                            Country / Region
                          </label>
                          <select
                            id="country"
                            name="country"
                            autoComplete="country"
                            className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                            required
                            onChange={this.handleChange}
                          >
                            <option>United States</option>
                            <option>Canada</option>
                            <option>Mexico</option>
                          </select>
                        </div>
                        <div className="col-span-6 sm:col-span-3">
                          <label htmlFor="company" className="block text-sm font-medium text-gray-700">
                            Company
                          </label>
                          <input
                            type="text"
                            name="company"
                            id="company"
                            autoComplete="company"
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                            onChange={this.handleChange}
                          />
                        </div>

                        <div className="col-span-6">
                          <label htmlFor="street_address" className="block text-sm font-medium text-gray-700">
                            Street address
                          </label>
                          <input
                            type="text"
                            name="street_address"
                            id="street_address"
                            autoComplete="street-address"
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                            onChange={this.handleChange}
                          />
                        </div>

                        <div className="col-span-6 sm:col-span-6 lg:col-span-2">
                          <label htmlFor="city" className="block text-sm font-medium text-gray-700">
                            City
                          </label>
                          <input
                            type="text"
                            name="city"
                            id="city"
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                            required
                            onChange={this.handleChange}
                          />
                        </div>

                        <div className="col-span-6 sm:col-span-3 lg:col-span-2">
                          <label htmlFor="state" className="block text-sm font-medium text-gray-700">
                            State / Province
                          </label>
                          <input
                            type="text"
                            name="state"
                            id="state"
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                            onChange={this.handleChange}
                          />
                        </div>

                        <div className="col-span-6 sm:col-span-3 lg:col-span-2">
                          <label htmlFor="postal_code" className="block text-sm font-medium text-gray-700">
                            ZIP / Postal
                          </label>
                          <input
                            type="text"
                            name="postal_code"
                            id="postal_code"
                            autoComplete="postal-code"
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                            onChange={this.handleChange}
                          />
                        </div>
                      </div>
                    </div>
                    <div className="px-4 py-3 bg-gray-50 text-right sm:px-6">
                      <button
                        type="submit"
                        className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                      >
                        Register
                      </button>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
          </motion.div>
     )
  }
}

export default SignUp
