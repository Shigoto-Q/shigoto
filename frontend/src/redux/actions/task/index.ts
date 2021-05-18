import { Dispatch } from "redux";
import { api } from "../../../api/";
import { TASK_CREATION_FAILED, TASK_CREATION_SUCCESS, TASK_RAN_SUCCESS } from "../../types/task/";

export const createTask = (
  taskName: string,
  crontab: number,
  kwargs: string,
  oneoff: boolean,
  enabled: boolean
) => async (dispatch: Dispatch) => {
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };
  const kw = {
    "request_endpoint": kwargs,
  }
  const body = {
    name: taskName,
    crontab: crontab,
    args: '',
    kwargs: JSON.stringify(kw),
    one_off: oneoff,
    enabled: enabled,
  };

  await api
    .post("/api/v1/task/", body, config)
    .then((res) => {
      dispatch({
        type: TASK_CREATION_SUCCESS,
        payload: res.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: TASK_CREATION_FAILED,
        payload: err.response,
      });
    });
};

export const runTask = (taskId: number) => async (dispatch: Dispatch) => {
  await api
    .get(`/api/v1/task/${taskId}/run/`)
    .then(res => {
      dispatch({
        type: TASK_RAN_SUCCESS,
        payload: res.data
      })
    })
}
