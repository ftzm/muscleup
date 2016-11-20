const API_ROOT = 'http://localhost:8000/api-v1/'

//Where actual fetching happens
function callApi(endpoint, inputJson = null) {

  let token = localStorage.getItem('id_token') || null
  let config = {}

  if (token) {
    config = {
      headers: new Headers({ Authorization: `JWT ${token}` }),
    }
  } else {
    throw 'No saved token'
  }

  if (inputJson !== null) {
    config.body = JSON.stringify(inputJson)
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

export default store => next => action => {

  const callAPI = action[CALL_API]

  if (typeof callAPI === 'undefined') {
    return next(action)
  }

  let { endpoint, inputJson, types } = callAPI

  const [requestType, successType, errorType] = types

  return callApi(endpoint, inputJson).then(
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
