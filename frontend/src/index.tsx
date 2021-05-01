import React, { lazy, Suspense } from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Spinner from "./components/Spinner"
import reportWebVitals from './reportWebVitals';
import axios from 'axios'
import 'react-toastify/dist/ReactToastify.css'
import { store } from "./redux/storeConfig/store"
import { Provider } from 'react-redux'

axios.defaults.baseURL = 'http://localhost:8000'
axios.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem("access")}`
const LazyApp = lazy(() => import('./App'))

ReactDOM.render(
  <Provider store={store}>
    <Suspense fallback={<Spinner />}>
      <React.StrictMode>
        <LazyApp />
      </React.StrictMode>
    </Suspense>
  </Provider>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
