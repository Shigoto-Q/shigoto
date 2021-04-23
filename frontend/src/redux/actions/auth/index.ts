import { Dispatch } from 'redux'

export const handleLogin = (data: any) => {
    return (dispatch: Dispatch) => {
        dispatch({type: "LOGIN", data})
        localStorage.setItem("userData", JSON.stringify(data))
    }
}

export const handleLogout = () => {
    return (dispatch: Dispatch) => {
        localStorage.removeItem("access")
        localStorage.removeItem("refresh")
    }
}
