import { combineReducers } from 'redux'
import exercises from './exercises'
import routines from './routines'
import routinedays from './routinedays'
import credentials from './credentials'
import errors from './errors'

const todoApp = combineReducers({
  credentials,
  exercises,
  routines,
  routinedays,
  errors,
})

export default todoApp
