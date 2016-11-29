import { CALL_API, API_POST, API_DELETE, API_PUT } from '../middleware/api'

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
      'ERROR_NEW',
    ],
  },
})

export const addExercise = (name, bodyweight) => ({
  [API_POST]: {
    endpoint: 'exercises/',
    types: [
      'EXERCISES_REQUEST',
      'EXERCISES_SUCCESS',
      'ERROR_NEW',
    ],
    inputJson: {
      name: name,

      //bodyweight: bodyweight,
    },
  },
})

export const renameExercise = (id, name) => ({
  [API_PUT]: {
    endpoint: 'exercises/' + id + '/',
    types: [
      'EXERCISES_REQUEST',
      'EXERCISES_RENAME',
      'ERROR_NEW',
    ],
    inputJson: {
      name: name,

      //bodyweight: bodyweight,
    },
  },
})

export const deleteExercise = (id) => ({
  [API_DELETE]: {
    endpoint: 'exercises/' + id + '/',
    id: id,
    types: [
      'EXERCISES_REQUEST',
      'EXERCISE_DELETED',
      'ERROR_NEW',
    ],
  },
})
