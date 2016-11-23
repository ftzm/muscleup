const API_ROOT = 'http://localhost:8000/api-v1/'

//Where actual fetching happens
function callApi(endpoint) {

  let token = localStorage.getItem('id_token') || null
  let config = {}

  if (token) {
    config = {
      headers: new Headers({ Authorization: `JWT ${token}` }),
    }
  } else {
    throw 'No saved token'
  }

  return fetch(API_ROOT + endpoint, config)
    .then(response =>
      response.json().then(json => {
        if (!response.ok) {
          return Promise.reject(json)
        }

        return json
      }).catch(e => console.log(e))
    )
}

function apiPost(endpoint, inputJson) {

  let token = localStorage.getItem('id_token') || null
  let config = {}

  if (token) {
    config = {
      method: 'POST',
      headers: new Headers({
        Authorization: `JWT ${token}`,
        'Content-Type': 'application/json',
      }),
      body: JSON.stringify(inputJson),
    }
  } else {
    throw 'No saved token'
  }

  return fetch(API_ROOT + endpoint, config)
    .then(response =>
      response.json().then(json => {
        if (!response.ok) {
          return Promise.reject(json)
        }

        return json
      }).catch(e => console.log(e))
    )
}

export const CALL_API = Symbol('Call API')

const callApiWrapper = (next, action) => {

  const callAPI = action[CALL_API]

  let { endpoint, types } = callAPI

  const [requestType, successType, errorType] = types

  return callApi(endpoint).then(
    response =>
      next({
        response,
        type: successType,
      }),
    error =>
      next({
        error: error.message || 'An error occurred.',
        type: errorType,
      })
  )
}

export const API_POST = Symbol('API POST')

const apiPostWrapper = (next, action) => {

  const APIPost = action[API_POST]

  let { endpoint, inputJson, types } = APIPost

  const [requestType, successType, errorType] = types

  return apiPost(endpoint, inputJson).then(
    response =>
      next({
        response,
        type: successType,
      }),
    error =>
      next({
        error: error.message || 'An error occurred.',
        type: errorType,
      })
  )
}

export default store => next => action => {
  if (typeof action[CALL_API] !== 'undefined') {
    callApiWrapper(next, action)
  } else if (typeof action[API_POST] !== 'undefined') {
    apiPostWrapper(next, action)
  } else {
    return next(action)
  }
}
