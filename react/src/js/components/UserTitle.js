import React, { PropTypes } from 'react'

const UserTitle = ({ email, token }) => {
  return (
          <div>
          <span>{email == '' ? 'Not Logged In' : `Email: ${email}`}</span>
          <br/>
          <span>token: {token}</span>
          </div>
  )
}

UserTitle.propTypes = {
  email: PropTypes.string.isRequired,
  token: PropTypes.string.isRequired,
}

export default UserTitle
