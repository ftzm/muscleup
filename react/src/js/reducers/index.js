import { combineReducers } from 'redux'
import exercises from './exercises'
import credentials from './credentials'

const todoApp = combineReducers({
  credentials,
  exercises
})

export default todoApp
