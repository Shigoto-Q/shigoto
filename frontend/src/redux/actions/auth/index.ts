import { Dispatch } from 'redux'
import { bareAPI } from "../../../api/"
import api from "../../../api/"
import {
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    LOGOUT,
    USER_LOADED_SUCCESS,
    USER_LOADED_FAIL,
    AUTHENTICATED_FAIL,
    AUTHENTICATED_SUCCESS,
    SIGNUP_FAIL,
    SIGNUP_SUCCESS
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
            const res = await api.post(`/auth/jwt/verify/`, body, config);
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
            const res = await api.get(`/auth/users/me/`, config);
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
    await bareAPI.post('/auth/jwt/create/', body, config)
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
type registerProps = {
    first_name: string,
    last_name: string,
    email_address: string,
    username: string,
    password: string,
    rePassword: string,
    country: string,
    company?: string,
    address: string,
    city: string,
    state?: string,
    postal_code: number
}

export const register = (props: registerProps) => async (dispatch: Dispatch) => {
    const config = {
        headers: {
            "Content-Type": "application/json"
        }
    }
    const body = {
        first_name: props.first_name,
        last_name: props.last_name,
        email: props.email_address,
        username: props.username,
        password: props.password,
        company: props.company,
        zip_code: props.postal_code,
        city: props.city,
        country: props.country
    }
    await bareAPI.post('/auth/users/', body, config)
        .then(res => {
            dispatch({
                type: SIGNUP_SUCCESS,
                payload: res.data
            })
        })
        .catch(err => {
            dispatch({
                type: SIGNUP_FAIL,
                payload: err.response
            })
        })
}
