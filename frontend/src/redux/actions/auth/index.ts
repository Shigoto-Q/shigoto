import { Dispatch } from 'redux'
import axios from 'axios'
import {
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  LOGOUT,
  USER_LOADED_SUCCESS,
  USER_LOADED_FAIL,
  AUTHENTICATED_FAIL,
  AUTHENTICATED_SUCCESS
} from '../../types/auth/';


export const checkAuthenticated = () => async (dispatch: Dispatch) => {
  if (typeof window == 'undefined') {
    dispatch({
      type: AUTHENTICATED_FAIL
    });
  }
  if (localStorage.getItem('access')) {
    const config = {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    };

    const body = JSON.stringify({ token: localStorage.getItem('access') });
    try {
      const res = await axios.post(`/auth/jwt/verify/`, body, config);
      if (res.data.code !== 'token_not_valid') {
        dispatch({
          type: AUTHENTICATED_SUCCESS
        });
      } else {
        dispatch({
          type: AUTHENTICATED_FAIL,
        });
      }
    } catch (err) {
      dispatch({
        type: AUTHENTICATED_FAIL
      });
    }
  } else {
    dispatch({
      type: AUTHENTICATED_FAIL
    });
  }
}
export const load_user = () => async (dispatch: Dispatch) => {
  if (localStorage.getItem('access')) {
    const config = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access')}`,
        'Accept': 'application/json'
      }
    };

    try {
      const res = await axios.get(`http://localhost:8000/auth/users/me/`, config);
      dispatch({
        type: USER_LOADED_SUCCESS,
        payload: res.data
      });
    } catch (err) {
      dispatch({
        type: USER_LOADED_FAIL
      });
    }
  } else {
    dispatch({
      type: USER_LOADED_FAIL
    });
  }

};


export const login = (username: string, password: string) => async (dispatch: Dispatch) => {
  const config = {
    headers: {
      "Content-Type": "application/json"
    }
  }
  const body = {
    username: username,
    password: password
  }

  await axios.post('/auth/jwt/create/', body, config)
    .then(res => {
      dispatch({
        type: LOGIN_SUCCESS,
        payload: res.data
      })
    })
    .catch(err => {
      dispatch({
        type: LOGIN_FAIL,
        payload: err.response
      })
    })
}
export const logout = () => (dispatch: Dispatch) => {
  dispatch({ type: LOGOUT });
}

export const handleLogout = () => {
  return (dispatch: Dispatch) => {
    localStorage.removeItem("access")
    localStorage.removeItem("refresh")
    localStorage.removeItem("userData")

  }
}
