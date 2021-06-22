import {
  SIGNUP_SUCCESS,
  SIGNUP_FAIL,
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  LOGOUT,
  AUTHENTICATED_FAIL,
  AUTHENTICATED_SUCCESS,
  USER_LOADED_SUCCESS,
  USER_LOADED_FAIL,
} from "../../types/auth/index";
import { toast, Slide } from "react-toastify";

const isUserAuth = localStorage.getItem("userData")

const initialState = {
  access: localStorage.getItem("access"),
  refresh: localStorage.getItem("refresh"),
  isAuthenticated: isUserAuth ? true : false,
  user: isUserAuth,
};

const reducers = (state = initialState, action: any) => {
  const { type, payload } = action;

  switch (type) {
    case AUTHENTICATED_SUCCESS:
      return {
        ...state,
        isAuthenticated: true,
      };
    case LOGIN_SUCCESS:
      localStorage.setItem("access", payload.access);
      localStorage.setItem("refresh", payload.refresh);
      toast("Logged in!", {
        transition: Slide,
        hideProgressBar: false,
        autoClose: 2000,
        closeOnClick: true,
        progress: undefined,
        pauseOnHover: false,
        pauseOnFocusLoss: false,
        draggable: true,
      });
      return {
        ...state,
        isAuthenticated: true,
        access: payload.access,
        refresh: payload.refresh,
      };
    case USER_LOADED_SUCCESS:
      localStorage.setItem("userData", JSON.stringify(payload));
      return {
        ...state,
        user: JSON.stringify(payload),
      };
    case SIGNUP_SUCCESS:
      toast("Account created successfully!", {
        position: "bottom-center",
        transition: Slide,
        hideProgressBar: false,
        autoClose: 2000,
        closeOnClick: true,
        progress: undefined,
        pauseOnHover: false,
        pauseOnFocusLoss: false,
        draggable: true,
      });
      return {
        ...state,
        isAuthenticated: false,
      };
    case AUTHENTICATED_FAIL:
      return {
        ...state,
        isAuthenticated: false,
      };
    case USER_LOADED_FAIL:
      return {
        ...state,
        user: null,
      };
    case SIGNUP_FAIL:
      return {
        ...state,
        isAuthenticated: false,
      }
    case LOGIN_FAIL:
      return {
        ...state,
        loginFail: true,
      };
    case LOGOUT:
      localStorage.removeItem("access")
      localStorage.removeItem("refresh")
      localStorage.removeItem("userData")
      localStorage.removeItem("githubAccess")
      toast("You've been logged out!", {
        transition: Slide,
        hideProgressBar: false,
        autoClose: 2000,
        closeOnClick: true,
        progress: undefined,
      });
      return {
        ...state,
        access: null,
        refresh: null,
        isAuthenticated: false,
        user: null,
      };
    default:
      return state;
  }
};

export default reducers;
