import {
  SIGNUP_SUCCESS,
  SIGNUP_FAIL,
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  LOGOUT,
  AUTHENTICATED_FAIL,
  AUTHENTICATED_SUCCESS,
  USER_LOADED_SUCCESS,
  USER_LOADED_FAIL
} from '../../types/auth/index'

const initialState = {
  access: "",
  refresh: "",
  isAuthenticated: false,
  user: "" 
}

const reducers = (state = initialState, action: any) => {
  const { type, payload } = action

  switch (type) {
    case AUTHENTICATED_SUCCESS:
      return {
        ...state,
        isAuthenticated: true
      }
    case LOGIN_SUCCESS:
      localStorage.setItem('access', payload.access)
      localStorage.setItem('refresh', payload.refresh)
      return {
        ...state,
        isAuthenticated: true,
        access: payload.access,
        refresh: payload.refresh
      }
    case USER_LOADED_SUCCESS:
      localStorage.setItem('userData', JSON.stringify(payload))
      return {
        ...state,
        user: payload
      }
    case SIGNUP_SUCCESS:
      return {
        ...state,
        isAuthenticated: false
      }
    case AUTHENTICATED_FAIL:
      return {
        ...state,
        isAuthenticated: false
      }
    case USER_LOADED_FAIL:
      return {
        ...state,
        user: null
      }
    case SIGNUP_FAIL:
    case LOGIN_FAIL:
      return {
        ...state,
        loginFail: true
      }
    case LOGOUT:
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      localStorage.removeItem('userData')
      return {
        ...state,
        access: null,
        refresh: null,
        isAuthenticated: false,
        user: null
      }
    default:
      return state
  }
}

export default reducers
