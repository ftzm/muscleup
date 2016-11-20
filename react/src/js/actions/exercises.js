import { CALL_API } from '../middleware/api'

export const requestExercises = () => ({
  type: 'REQUEST_EXERCISES',
})

export const receiveExercises = json => ({
  type: 'RECEIVE_EXERCISES',
  exercises: json,
})

export const fetchExercises = token => ({
  [CALL_API]: {
    endpoint: 'exercises/',
    types: [
      'EXERCISES_REQUEST',
      'EXERCISES_SUCCESS',
      'EXERCISES_FAILURE',
    ],
  },
})
