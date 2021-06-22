import { toast, Slide } from "react-toastify";
import {
  CRONTAB_CREATED,
  SCHEDULE_FAIL,
  INTERVAL_CREATED,
  SOLAR_CREATED,
  CLOCKED_CREATED,
} from "../../types/schedule/";


const loadUser = localStorage.getItem("userData") || "{}"
const initialState = {
  crontab: JSON.parse(loadUser).crontab,
};

const reducers = (state = initialState, action: any) => {
  const { type, payload } = action;

  switch (type) {
    case SCHEDULE_FAIL:
      return {
        ...state,
      };
    case CRONTAB_CREATED:
      toast("Crontab created successfully!", {
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
    case INTERVAL_CREATED:
      toast("Interval created successfully!", {
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
    case CLOCKED_CREATED:
      toast("Clock schedule created successfully!", {
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
    case SOLAR_CREATED:
      toast("Solar schedule created successfully!", {
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
