import React from 'react'
import { connect } from 'react-redux'
import { logout } from '../actions'

let Logout = ({ dispatch }) => {
  return (
    <div>
      <form onSubmit={e => {
        e.preventDefault()
        dispatch(logout())
        }}>
        <button type="submit">
          Logout
        </button>
      </form>
    </div>
  )
}
Logout = connect()(Logout)

export default Logout
