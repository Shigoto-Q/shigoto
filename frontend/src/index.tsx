import React, { lazy, Suspense } from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Spinner from "./components/Spinner"
import reportWebVitals from './reportWebVitals';
import 'react-toastify/dist/ReactToastify.css'
import {ToastContainer} from "react-toastify"
import { store } from "./redux/storeConfig/store"
import { Provider } from 'react-redux'

const LazyApp = lazy(() => import('./App'))

ReactDOM.render(
  <Provider store={store}>
    <Suspense fallback={<Spinner />}>
      <React.StrictMode>
        <LazyApp />
        <ToastContainer/>
      </React.StrictMode>
    </Suspense>
  </Provider>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
