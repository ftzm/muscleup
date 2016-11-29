import { combineReducers } from 'redux'
import exercises from './exercises'
import credentials from './credentials'
import errors from './errors'

const todoApp = combineReducers({
  credentials,
  exercises,
  errors,
})

export default todoApp
