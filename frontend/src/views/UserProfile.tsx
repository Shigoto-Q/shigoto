import { useState, useEffect } from "react";
import axios from "axios";
import { ghapi } from "../api";
import api from "../api";
import { GitHub } from "react-feather";
import SelectRepo from "../components/github/SelectRepos"

const UserSettings = () => {
  // eslint-disable-next-line
  const clientId = "37118d4f94826938834c";
  const clientSecret = "9c30e66a212af7f260dfa897a4387c8ddd928b72";
  const ghAuthUrl =
    "https://cors-anywhere.herokuapp.com/https://github.com/login/oauth/access_token";
  const userData = JSON.parse(localStorage.getItem("userData") || "{}");
  const [isGhConnected, setGhConnected] = useState(
    userData.github.token ? true : false
  );
  const [loading, setLoading] = useState(true)
  const [githubRepos, setGitHubRepos] = useState()
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
        Accept: "application/json",
      },
    };
    axios
      .post(ghAuthUrl, body, config)
      .then((res) => {
        localStorage.setItem("githubAccess", res.data.access_token);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const fetchRepos = () => {
    ghapi.get(userData.github.repos_urls).then((res) => {
      setGitHubRepos(res.data)
      setLoading(false)
    });
  };

  const getUserInfo = () => {
    ghapi.get("/user").then((res) => {
      const body = {
        login: res.data.login,
        avatar_url: res.data.avatar_url,
        repos_urls: res.data.repos_url,
        public_repos: res.data.public_repos,
        public_gists: res.data.public_gists,
        token: localStorage.getItem("githubAccess"),
      };
      api.post("api/v1/github/profile/", body);
    });
  };

  useEffect(() => {
    fetchRepos()
    if (isGhConnected) {
      const url = window.location.href;
      const hasCode = url.includes("?code=");
      if (hasCode) {
        const newUrl = url.split("?code=");
        window.history.pushState({}, "", newUrl[0]);
        const code = newUrl[1];
        setGhConnected(true);
        authrizeGithub(code);
        getUserInfo();
      }
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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
                        readOnly
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
                        readOnly
                        className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                      />
                    </div>

                    <div className="col-span-6 sm:col-span-3">
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
                        readOnly
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
                        defaultValue={userData.country}
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
                        readOnly
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
                        readOnly
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
                        readOnly
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
            </div>
          </div>
          <div className="shadow overflow-hidden sm:rounded-md">
            <div className="px-4 py-5 bg-white sm:p-6">
              <div className="grid grid-cols-3 gap-6">
                <div className="col-span-6 sm:col-span-6 lg:col-span-2">
                  <label
                    htmlFor="ghlogin"
                    className="block text-sm font-medium text-gray-700"
                  >
                    GitHub Username
                  </label>
                  <input
                    type="text"
                    name="github_user"
                    id="github_user"
                    value={userData.github.login}
                    readOnly
                    className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                  />
                </div>

                <div className="col-span-6 sm:col-span-3 lg:col-span-2">
                  <label
                    htmlFor="repos"
                    className="block text-sm font-medium text-gray-700"
                  >
                    Public repositories
                  </label>
                  <input
                    type="text"
                    name="public_repos"
                    id="public_repos"
                    value={userData.github.public_repos}
                    readOnly
                    className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                  />
                </div>

                <div className="col-span-6 sm:col-span-3 lg:col-span-2">
                  <label
                    htmlFor="gists"
                    className="block text-sm font-medium text-gray-700"
                  >
                    Public gists
                  </label>
                  <input
                    type="text"
                    name="public_gists"
                    id="public_gists"
                    autoComplete="postal-code"
                    value={userData.github.public_gists}
                    readOnly
                    className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                  />
                </div>
                <div className="col-span-6 sm:col-span-3">
                  <label
                    htmlFor="token"
                    className="block text-sm font-medium text-gray-700"
                  >
                    Token
                  </label>
                  <input
                    type="password"
                    name="token"
                    id="token"
                    autoComplete="postal-code"
                    value={userData.github.token}
                    readOnly
                    className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                  />
                </div>
              </div>
            </div>
            <div className="px-4 py-3 bg-gray-50 text-right sm:px-6">
              <a
                href={`https://github.com/login/oauth/authorize?client_id=${clientId}`}
                className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center"
              >
                <GitHub />
                <span>{isGhConnected ? "Connected" : "Connect"}</span>
              </a>
              <a
                href={`https://github.com/login/oauth/authorize?client_id=${clientId}`}
                className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center ml-4"
              >
                <GitHub />
                <span> Disconnect </span>
              </a>
            </div>
          </div>
          <div className="shadow overflow-hidden sm:rounded-md">
            <div className="px-4 py-5 bg-white sm:p-6">
              <div className="grid grid-cols-3 gap-6">
                <div className="col-span-6 sm:col-span-3 lg:col-span-2">
                  <label
                    htmlFor="repos"
                    className="block text-sm font-medium text-gray-700"
                  >
                    Public repositories
                  </label>
                  <input
                    type="text"
                    name="dpublic_repos"
                    id="dpublic_repos"
                    value={userData.github.public_repos}
                    readOnly
                    className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                  />
                </div>
              </div>
            </div>
            <div className="px-4 py-3 bg-gray-50 text-right sm:px-6">
                  {!loading ? <SelectRepo optionsProps={githubRepos} /> : ""}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default UserSettings;
