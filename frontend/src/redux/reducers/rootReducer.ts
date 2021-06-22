import { combineReducers } from 'redux'
import auth from './auth'
import schedule from './schedule'
import task from './task'
const rootReducer = combineReducers({
  auth,
  schedule,
  task,
})

export default rootReducer
