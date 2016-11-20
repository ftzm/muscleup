import React from 'react'
import { connect } from 'react-redux'
import { fetchToken } from '../actions'

let Login = ({ dispatch }) => {
  let email
  let password

  return (
    <div>
      <form onSubmit={e => {
        e.preventDefault()
        if (!email.value.trim()) {
          return
        }
        if (!password.value.trim()) {
          return
        }
        dispatch(fetchToken(email.value, password.value))
        email.value = ''
        password.value = ''
        }}>
        <input ref={node => {
          email = node
        }} />
        <input ref={node => {
          password = node
        }} />
        <button type="submit">
          Login
        </button>
      </form>
    </div>
  )
}
Login = connect()(Login)

export default Login
