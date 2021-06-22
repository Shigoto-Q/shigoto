import axios from 'axios'

const baseURL = "http://localhost:8000"

export const bareAPI = axios.create({
    baseURL: "http://localhost:8000"
})

const api = axios.create({
    baseURL: baseURL,
})


export const ghapi = axios.create({
    baseURL: "https://api.github.com",
    headers: { Authorization: `Token ${localStorage.getItem("githubAccess")}` }
})

ghapi.interceptors.request.use(
  config => {
    const token = localStorage.getItem("githubAccess")
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
)



api.interceptors.request.use(
  config => {
    const token = localStorage.getItem("access")
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
)


export default api
