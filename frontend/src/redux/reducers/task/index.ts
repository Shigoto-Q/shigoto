import { toast, Slide } from "react-toastify";
import {TASK_CREATION_FAILED, TASK_CREATION_SUCCESS, TASK_RAN_SUCCESS} from "../../types/task"

const initialState = {
  task: null
};

const reducers = (state = initialState, action: any) => {
  const { type, payload } = action;

  switch (type) {
    case TASK_CREATION_FAILED:
      return {
        ...state,
      };
    case TASK_CREATION_SUCCESS:
      toast("Task created successfully!", {
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
        crontab: payload,
      };
    case TASK_RAN_SUCCESS:
      toast("Task ran successfully!", {
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
        crontab: payload,
      };
    default:
      return state;
  }
};

export default reducers;
