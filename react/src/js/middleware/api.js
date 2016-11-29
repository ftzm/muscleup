const API_ROOT = 'http://localhost:8000/api-v1/'

function grabToken() {
  var token = localStorage.getItem('id_token') || null

  if (token) {
    return token
  } else {
    throw 'No saved token'
  }
}

function basicFetch(endpoint, config, types, next) {

  const [requestType, successType, errorType] = types

  return fetch(API_ROOT + endpoint, config)
    .then(response =>
      response.json().then(json => {
        if (!response.ok) {
          console.log('error on server end')
          return Promise.reject(JSON.stringify(json))
        }

        return json
      }), error => {
        console.log('network error?')
        return Promise.reject(error.toString())
      }
    ).then(
      response =>
      next({
        response,
        type: successType,
      }),
      error => {
        console.log('reached outer handler')
        console.log(error)
        next({
          message: error || 'An error occurred.',
          type: errorType,
        });
      }
    )
}

function post(next, action) {

  let { endpoint, inputJson, types } = action
  const [requestType, successType, errorType] = types

  let token = grabToken()

  let config = {
    method: 'POST',
    headers: new Headers({
      Authorization: `JWT ${token}`,
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify(inputJson),
  }

  return basicFetch(endpoint, config, types, next)
}

function put(next, action) {

  let { endpoint, inputJson, types } = action
  const [requestType, successType, errorType] = types

  let token = grabToken()

  let config = {
    method: 'PUT',
    headers: new Headers({
      Authorization: `JWT ${token}`,
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify(inputJson),
  }

  return basicFetch(endpoint, config, types, next)
}

function get(next, action) {

  let { endpoint, types } = action
  const [requestType, successType, errorType] = types

  let token = grabToken()

  let config = {
    headers: new Headers({ Authorization: `JWT ${token}` }),
  }

  return basicFetch(endpoint, config, types, next)
}

function apiDelete(next, action) {

  console.log('reached delete')

  let { endpoint, id, types } = action
  const [requestType, successType, errorType] = types

  let token = grabToken()

  let config = {
    method: 'DELETE',
    headers: new Headers({ Authorization: `JWT ${token}` }),
  }

  return fetch(API_ROOT + endpoint, config)
    .then(response => {
      if (response.status == 204) {
        next({
          id: id,
          type: successType,
        })
      } else {
        response.json().then(json => {
          console.log('not 204')
          next({
            message: JSON.stringify(json),
            type: errorType,
          })
        })
      }
    }).catch(e => {
      console.log('network error?')
      next({
        message: e.toString(),
        type: errorType,
      })
    })
}

export const CALL_API = Symbol('Call API')
export const API_POST = Symbol('API POST')
export const API_PUT = Symbol('API PUT')
export const API_DELETE = Symbol('API DELETE')

export default store => next => action => {
  if (typeof action[CALL_API] !== 'undefined') {
    get(next, action[CALL_API])
  } else if (typeof action[API_POST] !== 'undefined') {
    post(next, action[API_POST])
  } else if (typeof action[API_DELETE] !== 'undefined') {
    apiDelete(next, action[API_DELETE])
  } else if (typeof action[API_PUT] !== 'undefined') {
    put(next, action[API_PUT])
  } else {
    return next(action)
  }
}
