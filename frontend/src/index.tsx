import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import axios from 'axios'
import 'react-toastify/dist/ReactToastify.css'

axios.defaults.baseURL = 'http://localhost:8000'
axios.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem("access")}`
axios.interceptors.response.use((response: any) => {
            return response
            }, (err: any) => {
            return new Promise((resolve: any, reject: any) => {
                        const originalReq = err.config 
                        if ( err.response.status === 401 && err.config && !err.config._isRetryRequest ) {
                            originalReq._retry = true

                            let res = fetch('http://localhost:8000/auth/jwt/refresh/', {
                                method: 'POST',
                                mode: 'cors',
                                cache: 'no-cache',
                                credentials: 'same-origin',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'Authorization': `Bearer ${localStorage.getItem("access")}`
                                },
                                redirect: 'follow',
                                referrer: 'no-referrer',
                                body: JSON.stringify({
                                    "refresh": localStorage.getItem("refresh")
                                        })
                                }).then(res => res.json()).then(res => {
                                    console.log(res)
                                    originalReq.headers["Authorization"] = `Bearer ${res.access}`
                                    localStorage.setItem("access", res.access)
                                    return axios(originalReq)
                                    })
                                    resolve(res)
                        }
                        return Promise.reject(err)
                    })

            })
ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
