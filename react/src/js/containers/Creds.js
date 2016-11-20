import React from 'react'
import { connect } from 'react-redux'
import Login from '../containers/Login'
import Logout from '../containers/Logout'
import User from '../containers/User'

const mapStateToProps = (state) => {
  return {
    token: state.credentials.token
  }
}

let Creds = ({ token }) => (
  <div>
    <User />
    {token == '' ? <Login /> : <Logout />}
  </div>
)

Creds = connect(
  mapStateToProps
)(Creds)

export default Creds
