import { connect } from 'react-redux'
import UserTitle from '../components/UserTitle'

const mapStateToProps = (state) => {
  return {
    email: state.credentials.email,
    token: state.credentials.token
  }
}

const User = connect(
  mapStateToProps
)(UserTitle)

export default User
