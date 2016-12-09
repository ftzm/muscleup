import { CALL_API, API_POST, API_DELETE, API_PUT } from '../middleware/api'
import { apiGet, apiPut, apiPost, apiDelete } from '../api/api'

const requestExercises = () => ({
  type: 'EXERCISES_REQUEST',
})

const requestExercisesFailure = () => ({
  type: 'EXERCISES_REQUEST_FAILURE',
})

const receiveExercises = json => ({
  type: 'EXERCISES_SUCCESS',
  response: json,
})

export function fetchExercises() {
  return function (dispatch) {
    dispatch(requestExercises())
    return apiGet('exercises/').then(
      p => dispatch(receiveExercises(p)),
      e => {
        dispatch(requestExercisesFailure())
        dispatch({ type: 'ERROR_NEW', message: e })
      }
    )
  }
}

const shouldFetchExercises = (state) => {
  console.log(state.exercises.get('exercises'))

  //console.log(exercises)
  /*posts = state.postsByReddit[reddit]
  if (!posts) {
    return true
  }

  if (posts.isFetching) {
    return false
  }

  return posts.didInvalidate*/
  return true
}

export const fetchExercisesIfNeeded = () => (dispatch, getState) => {
  if (shouldFetchExercises(getState())) {
    return dispatch(fetchExercises())
  }
}

const saveExerciseRename = json => ({
  type: 'EXERCISE_RENAMED',
  response: json,
})

export function renameExercise(id, name) {
  return function (dispatch) {
    const endpoint = 'exercises/' + id + '/'
    const inputJson = {
      name: name,
    }
    return apiPut(endpoint, inputJson).then(
      p => dispatch(saveExerciseRename(p)),
      e => dispatch({ type: 'ERROR_NEW', message: e })
    )
  }
}

const addExerciseSuccess = json => ({
  type: 'EXERCISE_ADDED',
  response: json,
})

export function addExercise(name) {
  return function (dispatch) {
    const inputJson = {
      name: name,
    }
    return apiPost('exercises/', inputJson).then(
      p => dispatch(addExerciseSuccess(p)),
      e => dispatch({ type: 'ERROR_NEW', message: e })
    )
  }
}

const deleteExerciseSuccess = id => ({
  type: 'EXERCISE_DELETED',
  id: id,
})

export function deleteExercise(id) {
  return function (dispatch) {
    const endpoint = 'exercises/' + id + '/'
    return apiDelete(endpoint, id).then(
      p => dispatch(deleteExerciseSuccess(id)),
      e => dispatch({ type: 'ERROR_NEW', message: e })
    )
  }
}
