import { Dispatch } from "redux";
import api from "../../../api/";
import {TASK_CREATION_FAILED, TASK_CREATION_SUCCESS, TASK_DELETE_SUCCESS, TASK_RAN_SUCCESS} from "../../types/task/";

type Kwargs = {
  requestEndpoint: string;
  repoUrl: string,
  repoName: string,
  imageName: string;
  command: string;
}

export const createTask = (
  taskName: string,
  task: string,
  crontab: number,
  kwargs: Kwargs,
  oneoff: boolean,
  enabled: boolean
) => async (dispatch: Dispatch) => {
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };
  let kw = {}
  let taskType = undefined;
  if(task === "custom_endpoint") {
    taskType = 1
    kw = {
      "request_endpoint": kwargs.requestEndpoint
    }
  } else if (task === "k8s_job") {
    taskType = 2
    kw = {
      "repo_url" : kwargs.repoUrl,
      "full_name" : kwargs.repoName,
      "image_name": kwargs.imageName,
      "command": kwargs.command
    }
  }


  const body = {
    name: taskName,
    task: task,
    task_type: taskType,
    crontab: crontab,
    args: '',
    kwargs: JSON.stringify(kw),
    one_off: oneoff,
    enabled: enabled,
  };

  console.log(kw)


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

export const deleteTask = (taskId: number) => async (dispatch: Dispatch) => {
  await api.delete(`/api/v1/task/${taskId}/delete/`)
      .then(res => {
        dispatch({
          type: TASK_DELETE_SUCCESS,
          payload: res.data
        })
      })
}
