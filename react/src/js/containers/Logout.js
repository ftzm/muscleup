import React from 'react'
import { connect } from 'react-redux'
import { logout } from '../actions'
import { Map } from 'immutable'


let Logout = ({ dispatch }) => {
  console.log(testMap)
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
