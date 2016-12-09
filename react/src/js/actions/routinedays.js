import {
  apiGet,
  apiPut,
  apiPost,
  apiDelete
} from '../api/api'

const requestRoutinedays = () => ({
  type: 'ROUTINEDAYS_REQUEST',
})

const requestRoutinedaysFailure = () => ({
  type: 'ROUTINEDAYS_REQUEST_FAILURE',
})

const receiveRoutinedays = (json, id) => ({
  type: 'ROUTINEDAYS_SUCCESS',
  response: json,
  routine: id,
})

export function fetchRoutinedays(id) {
  console.log("going for routinedays")
  return function(dispatch) {
    dispatch(requestRoutinedays())
    let endpoint = 'routines/' + id + '/routinedays/'
    return apiGet(endpoint)
      .then(
        p => {
          console.log("fetched routinedays")
          console.log(p)
          dispatch(receiveRoutinedays(p, id))
        },
        e => {
          console.log("routinedays error")
          dispatch(requestRoutinedaysFailure())
          dispatch({
            type: 'ERROR_NEW',
            message: e,
          })
        }
      )
  }
}

const shouldFetchRoutinedays = (state) => {
  console.log(state.routinedays.get('routinedays'))

  return true
}

export const fetchRoutinedaysIfNeeded = () => (dispatch, getState) => {
  if (shouldFetchRoutinedays(getState())) {
    return dispatch(fetchRoutinedays())
  }
}

const saveRoutinedayRename = json => ({
  type: 'ROUTINEDAY_RENAMED',
  response: json,
})

export function renameRoutineday(id, name) {
  return function(dispatch) {
    const endpoint = 'routinedays/' + id + '/'
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

const addRoutinedaySuccess = json => ({
  type: 'ROUTINEDAY_ADDED',
  response: json,
})

export function addRoutineday(name, length, position) {
  return function(dispatch) {
    const inputJson = {
      name: name,
      cycle_length: length,
      cycle_position: position,
    }
    return apiPost('routinedays/', inputJson)
      .then(
        p => dispatch(addRoutinedaySuccess(p)),
        e => dispatch({
          type: 'ERROR_NEW',
          message: e
        })
      )
  }
}

const deleteRoutinedaySuccess = id => ({
  type: 'ROUTINEDAY_DELETED',
  id: id,
})

export function deleteRoutineday(id) {
  return function(dispatch) {
    const endpoint = 'routinedays/' + id + '/'
    return apiDelete(endpoint, id)
      .then(
        () => dispatch(deleteRoutinedaySuccess(id)),
        e => dispatch({
          type: 'ERROR_NEW',
          message: e
        })
      )
  }
}
