import {
  apiGet,
  apiPut,
  apiPost,
  apiDelete
} from '../api/api'

const requestRoutines = () => ({
  type: 'ROUTINES_REQUEST',
})

const requestRoutinesFailure = () => ({
  type: 'ROUTINES_REQUEST_FAILURE',
})

const receiveRoutines = json => ({
  type: 'ROUTINES_SUCCESS',
  response: json,
})

export function fetchRoutines() {
  return function(dispatch) {
    dispatch(requestRoutines())
    return apiGet('routinesexpanded/')
      .then(
        p => {
          console.log(p)
          dispatch(receiveRoutines(p))
        },
        e => {
          dispatch(requestRoutinesFailure())
          dispatch({
            type: 'ERROR_NEW',
            message: e,
          })
        }
      )
  }
}

const shouldFetchRoutines = (state) => {
  console.log(state.routines.get('routines'))

  return true
}

export const fetchRoutinesIfNeeded = () => (dispatch, getState) => {
  if (shouldFetchRoutines(getState())) {
    return dispatch(fetchRoutines())
  }
}

const saveRoutineRename = json => ({
  type: 'ROUTINE_RENAMED',
  response: json,
})

export function renameRoutine(id, name) {
  return function(dispatch) {
    const endpoint = 'routines/' + id + '/'
    const inputJson = {
      name: name,
    }
    return apiPut(endpoint, inputJson)
      .then(
        p => dispatch(saveRoutineRename(p)),
        e => dispatch({
          type: 'ERROR_NEW',
          message: e
        })
      )
  }
}

const addRoutineSuccess = json => ({
  type: 'ROUTINE_ADDED',
  response: json,
})

export function addRoutine(name, length, position) {
  return function(dispatch) {
    const inputJson = {
      name: name,
      cycle_length: length,
      cycle_position: position,
    }
    return apiPost('routines/', inputJson)
      .then(
        p => dispatch(addRoutineSuccess(p)),
        e => dispatch({
          type: 'ERROR_NEW',
          message: e
        })
      )
  }
}

const deleteRoutineSuccess = id => ({
  type: 'ROUTINE_DELETED',
  id: id,
})

export function deleteRoutine(id) {
  return function(dispatch) {
    const endpoint = 'routines/' + id + '/'
    return apiDelete(endpoint, id)
      .then(
        p => dispatch(deleteRoutineSuccess(id)),
        e => dispatch({
          type: 'ERROR_NEW',
          message: e
        })
      )
  }
}

const addRoutinedaySuccess = json => ({
  type: 'ROUTINEDAY_ADDED',
  json: json,
})

export function addRoutineday(name, routine, position) {
  return function(dispatch) {
    console.log('addRoutineday')
    const inputJson = {
      name,
      routine,
      position,
    }
    const endpoint = 'routines/' + routine + '/routinedays/'
    return apiPost(endpoint, inputJson)
      .then(
        p => dispatch(addRoutinedaySuccess(p)),
        e => dispatch({
          type: 'ERROR_NEW',
          message: e
        })
      )
  }
}

const deleteRoutinedaySuccess = (routine, routineday) => ({
  type: 'ROUTINEDAY_DELETED',
  routine,
  routineday,
})

export function deleteRoutineday(routine, routineday) {
  return function(dispatch) {
    const endpoint = 'routines/' + routine + '/routinedays/' + routineday + '/'
    return apiDelete(endpoint, routineday)
      .then(
        p => dispatch(deleteRoutinedaySuccess(routine, routineday)),
        e => dispatch({
          type: 'ERROR_NEW',
          message: e
        })
      )
  }
}

const saveRoutinedayRename = json => ({
  type: 'ROUTINEDAY_RENAMED',
  response: json,
})

export function renameRoutineday(routine, routineday, name) {
  return function(dispatch) {
    const endpoint = 'routines/' + routine + '/routinedays/' + routineday + '/'
    const inputJson = {
      name: name,
    }
    return apiPut(endpoint, inputJson)
      .then(
        p => dispatch(saveRoutinedayRename(p)),
        e => dispatch({
          type: 'ERROR_NEW',
          message: e
        })
      )
  }
}
