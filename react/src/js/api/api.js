const API_ROOT = 'http://localhost:8000/api-v1/'

function grabToken() {
  var token = localStorage.getItem('id_token') || null

  if (token) {
    return token
  } else {
    throw 'No saved token'
  }
}

function basicFetch(endpoint, config) {

  return fetch(API_ROOT + endpoint, config)
    .then(response =>
      response.json().then(json => {
        if (!response.ok) {
          console.log('error on server end')
          console.log(response)
          return Promise.reject(JSON.stringify(json))
        }

        return json
      }), error => {
        console.log('network error?')
        return Promise.reject(error.toString())
      })
}

export function apiPost(endpoint, inputJson) {

  let token = grabToken()

  let config = {
    method: 'POST',
    headers: new Headers({
      Authorization: `JWT ${token}`,
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify(inputJson),
  }

  return basicFetch(endpoint, config)
}

export function apiPut(endpoint, inputJson) {

  let token = grabToken()

  let config = {
    method: 'PATCH',
    headers: new Headers({
      Authorization: `JWT ${token}`,
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify(inputJson),
  }

  return basicFetch(endpoint, config)
}

export function apiGet(endpoint) {

  let token = grabToken()

  let config = {
    headers: new Headers({ Authorization: `JWT ${token}` }),
  }

  return basicFetch(endpoint, config)
}

export function apiDelete(endpoint, id) {

  let token = grabToken()

  let config = {
    method: 'DELETE',
    headers: new Headers({ Authorization: `JWT ${token}` }),
  }

  return fetch(API_ROOT + endpoint, config)
    .then(
      response => {
        if (response.status != 204) {
          console.log(response)
          throw 'Deletion failure'
        } else {
          return id
        }
      },

    e => {
      console.log('outer delete fail')
      throw e.toString()
    })
}
