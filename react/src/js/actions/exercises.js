import { CALL_API, API_POST } from '../middleware/api'

export const requestExercises = () => ({
  type: 'REQUEST_EXERCISES',
})

export const receiveExercises = json => ({
  type: 'RECEIVE_EXERCISES',
  exercises: json,
})

export const fetchExercises = () => ({
  [CALL_API]: {
    endpoint: 'exercises/',
    types: [
      'EXERCISES_REQUEST',
      'EXERCISES_SUCCESS',
      'EXERCISES_FAILURE',
    ],
  },
})

export const addExercise = (name, bodyweight) => ({
  [API_POST]: {
    endpoint: 'exercises/',
    types: [
      'EXERCISES_REQUEST',
      'EXERCISES_SUCCESS',
      'EXERCISES_FAILURE',
    ],
    inputJson: {
      name: name,

      //bodyweight: bodyweight,
    },
  },
})
