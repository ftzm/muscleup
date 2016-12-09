import { CALL_API } from '../middleware/api'

export function login(email, password) {
  return {
    type: 'LOGIN',
    email,
    password,
  }
}

export const logout = () => ({
  type: 'LOGOUT',
})

export function requestToken(email, password) {
  return {
    type: 'REQUEST_TOKEN',
    email,
    password,
  }
}

export function receiveToken(email, token) {
  return {
    type: 'RECEIVE_TOKEN',
    email: email,
    token: token,
  }
}

export function failedLogin() {
  return {
    type: 'FAILED_LOGIN',
  }
}

export function errorNew(message) {
  return {
    type: 'ERROR_NEW',
    message: message,
  }
}

export function errorTimeout() {
  return {
    type: 'ERROR_TIMEOUT',
  }
}

export function fetchToken(email, password) {
  return function (dispatch) {
    return fetch('http://localhost:8000/api-token-auth/', {
      method: 'POST',
      headers: new Headers({
        'Content-Type': 'application/json',
      }),
      body: JSON.stringify({
        email: email,
        password: password,
      }), })
      .then(
        response => response.json()
      )
      .then(json => {
        if ('token' in json) {
          localStorage.setItem('id_token', json.token)
          dispatch(errorNew('logged in'))
          dispatch(receiveToken(email, json.token))
        } else {
          dispatch(receiveToken('loger', ''))
        }
      })
      .catch(e => dispatch(receiveToken('ne', '')))
  }
}

