import { combineReducers } from 'redux'
import exercises from './exercises'
import routines from './routines'
import credentials from './credentials'
import errors from './errors'

const todoApp = combineReducers({
  credentials,
  exercises,
  routines,
  errors,
})

export default todoApp
