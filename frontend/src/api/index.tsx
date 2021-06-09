import axios from 'axios'

export const bareAPI = axios.create({
  baseURL: "http://localhost:8000"
})

export const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {Authorization: `Bearer ${localStorage.getItem("access")}`}
})

export const ghapi = axios.create({
  baseURL: "https://api.github.com",
  headers: { Authorization: `Token ${localStorage.getItem("githubAccess")}` }
    })
