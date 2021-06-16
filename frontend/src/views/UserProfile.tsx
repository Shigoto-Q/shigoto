import { useState, useEffect } from "react";
import axios from "axios";
import { ghapi, api } from "../api"
import { GitHub } from "react-feather"

const UserSettings = () => {
    // eslint-disable-next-line
    const clientId = "37118d4f94826938834c";
    const clientSecret = "9c30e66a212af7f260dfa897a4387c8ddd928b72";
    const ghAuthUrl =
        "https://cors-anywhere.herokuapp.com/https://github.com/login/oauth/access_token";
    const [isGhConnected, setGhConnected] = useState(true ? localStorage.getItem("githubAccess") : false);
    const userData = JSON.parse(localStorage.getItem("userData") || "{}");
    const [data, setData] = useState({ errorMessage: "", isLoading: false });
    const authrizeGithub = (code: string) => {
        const body = {
            client_id: clientId,
            client_secret: clientSecret,
            code: code,
            redirect_uri: "http://localhost:3000/dashboard/profile-settings",
        };
        const config = {
            headers: {
                "Access-Control-Allow-Origin": "*",
                Accept: "application/json"
            },
        };
        axios
            .post(ghAuthUrl, body, config)
            .then((res) => {
                localStorage.setItem(
                    "githubAccess",
                    res.data.access_token)

            })
            .catch((err) => {
                console.log(err);
            });
    };

    const getUserInfo = () => {
        ghapi.get("/user")
            .then(res => {
                const body = {
                    login: res.data.login,
                    avatar_url: res.data.avatar_url,
                    repos_urls: res.data.repos_urls,
                    public_repos: res.data.public_repos,
                    public_gists: res.data.public_gists,
                    token: localStorage.getItem("githubAccess")
                }
                api.post("api/v1/github/profile/", body)
                    .then(resp => { })
                    .catch(error => { })

                console.log(res)
            })
            .catch(err => {
                console.log(err)
            })
    }

    useEffect(() => {
        const url = window.location.href;
        const hasCode = url.includes("?code=");
        if (hasCode) {
            const newUrl = url.split("?code=");
            window.history.pushState({}, "", newUrl[0]);
            const code = newUrl[1];
            setGhConnected(true)
            authrizeGithub(code);
        }
    }, []);

    useEffect(() => {
        getUserInfo()
    }, [])

    return (
        <>
            <div className="mt-10 sm:mt-0">
                <div className="md:grid md:grid-cols-3 md:gap-6">
                    <div className="md:col-span-1">
                        <div className="px-4 sm:px-0">
                            <h3 className="text-lg font-medium leading-6 text-gray-900">
                                Personal Information
              </h3>
                            <p className="mt-1 text-sm text-gray-600">
                                Use a permanent address where you can receive mail.
              </p>
                        </div>
                    </div>
                    <div className="mt-5 md:mt-0 md:col-span-2">
                        <form action="#" method="POST">
                            <div className="shadow overflow-hidden sm:rounded-md">
                                <div className="px-4 py-5 bg-white sm:p-6">
                                    <div className="grid grid-cols-6 gap-6">
                                        <div className="col-span-6 sm:col-span-3">
                                            <label
                                                htmlFor="first_name"
                                                className="block text-sm font-medium text-gray-700"
                                            >
                                                First name
                      </label>
                                            <input
                                                type="text"
                                                name="first_name"
                                                id="first_name"
                                                autoComplete="given-name"
                                                value={userData.first_name}
                                                className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                            />
                                        </div>

                                        <div className="col-span-6 sm:col-span-3">
                                            <label
                                                htmlFor="last_name"
                                                className="block text-sm font-medium text-gray-700"
                                            >
                                                Last name
                      </label>
                                            <input
                                                type="text"
                                                name="last_name"
                                                id="last_name"
                                                autoComplete="family-name"
                                                value={userData.last_name}
                                                className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                            />
                                        </div>

                                        <div className="col-span-6 sm:col-span-4">
                                            <label
                                                htmlFor="email_address"
                                                className="block text-sm font-medium text-gray-700"
                                            >
                                                Email address
                      </label>
                                            <input
                                                type="text"
                                                name="email_address"
                                                id="email_address"
                                                autoComplete="email"
                                                value={userData.email}
                                                className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                            />
                                        </div>

                                        <div className="col-span-6 sm:col-span-3">
                                            <label
                                                htmlFor="country"
                                                className="block text-sm font-medium text-gray-700"
                                            >
                                                Country / Region
                      </label>
                                            <select
                                                id="country"
                                                name="country"
                                                autoComplete="country"
                                                value={userData.country}
                                                className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                            >
                                                <option>United States</option>
                                                <option>Canada</option>
                                                <option>Mexico</option>
                                            </select>
                                        </div>

                                        <div className="col-span-6">
                                            <label
                                                htmlFor="street_address"
                                                className="block text-sm font-medium text-gray-700"
                                            >
                                                Street address
                      </label>
                                            <input
                                                type="text"
                                                name="street_address"
                                                id="street_address"
                                                autoComplete="street-address"
                                                className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                            />
                                        </div>

                                        <div className="col-span-6 sm:col-span-6 lg:col-span-2">
                                            <label
                                                htmlFor="city"
                                                className="block text-sm font-medium text-gray-700"
                                            >
                                                City
                      </label>
                                            <input
                                                type="text"
                                                name="city"
                                                id="city"
                                                value={userData.city}
                                                className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                            />
                                        </div>

                                        <div className="col-span-6 sm:col-span-3 lg:col-span-2">
                                            <label
                                                htmlFor="state"
                                                className="block text-sm font-medium text-gray-700"
                                            >
                                                State / Province
                      </label>
                                            <input
                                                type="text"
                                                name="state"
                                                id="state"
                                                value={userData.state}
                                                className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                            />
                                        </div>

                                        <div className="col-span-6 sm:col-span-3 lg:col-span-2">
                                            <label
                                                htmlFor="postal_code"
                                                className="block text-sm font-medium text-gray-700"
                                            >
                                                ZIP / Postal
                      </label>
                                            <input
                                                type="text"
                                                name="postal_code"
                                                id="postal_code"
                                                autoComplete="postal-code"
                                                value={userData.zip_code}
                                                className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                            />
                                        </div>
                                    </div>
                                </div>
                                <div className="px-4 py-3 bg-gray-50 text-right sm:px-6">
                                    <button
                                        type="submit"
                                        className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                                    >
                                        Save
                  </button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            <div className="hidden sm:block" aria-hidden="true">
                <div className="py-5">
                    <div className="border-t border-gray-200" />
                </div>
            </div>
            <div>
                <div className="md:grid md:grid-cols-3 md:gap-6">
                    <div className="md:col-span-1">
                        <div className="px-4 sm:px-0">
                            <h3 className="mt-5 text-lg font-medium leading-6 text-gray-900">
                                Github
              </h3>
                            <p className="mt-1 mb-4 text-sm text-gray-600">
                                Connect your github profile for easy access to your code.
              </p>
                            <a
                                href={`https://github.com/login/oauth/authorize?client_id=${clientId}`}
                            >
                                <GitHub />
                            </a>
                        </div>
                    </div>
                    <div className="mt-5 md:mt-0 md:col-span-2">
                        <form action="#" method="POST">
                            <div className="shadow sm:rounded-md sm:overflow-hidden">
                                <div className="px-4 py-5 bg-white space-y-6 sm:p-6">
                                    <div className="grid grid-cols-3 gap-6">
                                        <div className="col-span-3 sm:col-span-2">
                                            <label
                                                htmlFor="company_website"
                                                className="block text-sm font-medium text-gray-700"
                                            >
                                                Website
                      </label>
                                            <div className="mt-1 flex rounded-md shadow-sm">
                                                <span className="inline-flex items-center px-3 rounded-l-md border border-r-0 border-gray-300 bg-gray-50 text-gray-500 text-sm">
                                                    http://
                        </span>
                                                <input
                                                    type="text"
                                                    name="company_website"
                                                    id="company_website"
                                                    className="focus:ring-indigo-500 focus:border-indigo-500 flex-1 block w-full rounded-none rounded-r-md sm:text-sm border-gray-300"
                                                    placeholder="www.github.com"
                                                />
                                            </div>
                                        </div>
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700">
                                            Photo
                    </label>
                                        <div className="mt-1 flex items-center">
                                            <span className="inline-block h-12 w-12 rounded-full overflow-hidden bg-gray-100">
                                                <svg
                                                    className="h-full w-full text-gray-300"
                                                    fill="currentColor"
                                                    viewBox="0 0 24 24"
                                                >
                                                    <path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 11.996 5.993zM16.002 8.999a4 4 0 11-8 0 4 4 0 018 0z" />
                                                </svg>
                                            </span>
                                            <button
                                                type="button"
                                                className="ml-5 bg-white py-2 px-3 border border-gray-300 rounded-md shadow-sm text-sm leading-4 font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                                            >
                                                Change
                      </button>
                                        </div>
                                    </div>
                                </div>
                                <div className="px-4 py-3 bg-gray-50 text-right sm:px-6">
                                    <button
                                        type="submit"
                                        className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                                    >
                                        Save
                  </button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            <div className="hidden sm:block" aria-hidden="true">
                <div className="py-5">
                    <div className="border-t border-gray-200" />
                </div>
            </div>

            <div className="mt-10 sm:mt-0">
                <div className="md:grid md:grid-cols-3 md:gap-6">
                    <div className="md:col-span-1">
                        <div className="px-4 sm:px-0">
                            <h3 className="text-lg font-medium leading-6 text-gray-900">
                                Notifications
              </h3>
                            <p className="mt-1 text-sm text-gray-600">
                                Decide which communications you'd like to receive and how.
              </p>
                        </div>
                    </div>
                    <div className="mt-5 md:mt-0 md:col-span-2">
                        <form action="#" method="POST">
                            <div className="shadow overflow-hidden sm:rounded-md">
                                <div className="px-4 py-5 bg-white space-y-6 sm:p-6">
                                    <fieldset>
                                        <legend className="text-base font-medium text-gray-900">
                                            By Email
                    </legend>
                                        <div className="mt-4 space-y-4">
                                            <div className="flex items-start">
                                                <div className="flex items-center h-5">
                                                    <input
                                                        id="comments"
                                                        name="comments"
                                                        type="checkbox"
                                                        className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                                                    />
                                                </div>
                                                <div className="ml-3 text-sm">
                                                    <label
                                                        htmlFor="comments"
                                                        className="font-medium text-gray-700"
                                                    >
                                                        Comments
                          </label>
                                                    <p className="text-gray-500">
                                                        Get notified when a task finishes.
                          </p>
                                                </div>
                                            </div>
                                            <div className="flex items-start">
                                                <div className="flex items-center h-5">
                                                    <input
                                                        id="candidates"
                                                        name="candidates"
                                                        type="checkbox"
                                                        className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                                                    />
                                                </div>
                                                <div className="ml-3 text-sm">
                                                    <label
                                                        htmlFor="candidates"
                                                        className="font-medium text-gray-700"
                                                    >
                                                        Candidates
                          </label>
                                                    <p className="text-gray-500">
                                                        Get notified when a task succeds.
                          </p>
                                                </div>
                                            </div>
                                            <div className="flex items-start">
                                                <div className="flex items-center h-5">
                                                    <input
                                                        id="offers"
                                                        name="offers"
                                                        type="checkbox"
                                                        className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                                                    />
                                                </div>
                                                <div className="ml-3 text-sm">
                                                    <label
                                                        htmlFor="offers"
                                                        className="font-medium text-gray-700"
                                                    >
                                                        Offers
                          </label>
                                                    <p className="text-gray-500">
                                                        Get notified when a task fails.
                          </p>
                                                </div>
                                            </div>
                                        </div>
                                    </fieldset>
                                </div>
                                <div className="px-4 py-3 bg-gray-50 text-right sm:px-6">
                                    <button
                                        type="submit"
                                        className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                                    >
                                        Save
                                        Save
                  </button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
                <div className="hidden sm:block" aria-hidden="true">
                    <div className="py-5">
                        <div className="border-t border-gray-200" />
                    </div>
                </div>
            </div>
        </>
    );
};

export default UserSettings;
