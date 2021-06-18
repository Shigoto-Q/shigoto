import { Dispatch } from "redux";
import api from "../../../api/";
import {
  SOLAR_CREATED,
  CRONTAB_CREATED,
  CLOCKED_CREATED,
  INTERVAL_CREATED,
  SCHEDULE_FAIL,
} from "../../types/schedule/";

export const createCrontab = (crons: Array<String>) => async (
  dispatch: Dispatch
) => {
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };
  const body = {
    minute: crons[0],
    hour: crons[1],
    day_of_month: crons[2],
    month_of_year: crons[3],
    day_of_week: crons[4],
  };
  await api
    .post("/api/v1/schedule/cron/", body, config)
    .then((res) => {
      dispatch({
        type: CRONTAB_CREATED,
        payload: res.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: SCHEDULE_FAIL,
        payload: err.response,
      });
    });
};

export const createInterval = (every: number, period: string) => async (
  dispatch: Dispatch
) => {
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };
  const body = {
    every: every,
    period: period,
  };
  await api
    .post("/api/v1/schedule/interval/", body, config)
    .then((res) => {
      dispatch({
        type: INTERVAL_CREATED,
        payload: res.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: SCHEDULE_FAIL,
        payload: err.response,
      });
    });
};

export const createClocked = (clocked: string) => async (
  dispatch: Dispatch
) => {
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };
  const body = {
    clocked_time: clocked,
  };
  await api
    .post("/api/v1/schedule/clock/", body, config)
    .then((res) => {
      dispatch({
        type: CLOCKED_CREATED,
        payload: res.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: SCHEDULE_FAIL,
        payload: err.response,
      });
    });
};

export const createSolar = (
  event: string,
  latitude: string,
  longitude: string
) => async (dispatch: Dispatch) => {
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };
  const body = {
    event: event,
    latitude: latitude,
    longitude: longitude,
  };
  await api
    .post("/api/v1/schedule/solar/", body, config)
    .then((res) => {
      dispatch({
        type: SOLAR_CREATED,
        payload: res.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: SCHEDULE_FAIL,
        payload: err.response,
      });
    });
};
