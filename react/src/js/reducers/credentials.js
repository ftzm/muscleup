const credentials = (state = {
  email: '',
  token: ''
}, action) => {
  switch (action.type) {
    case 'LOGIN':
      return {email: action.email, token: ''}
    case 'LOGOUT':
      return {email: '', token: ''}
    case 'RECEIVE_TOKEN':
      return {email: action.email, token: action.token}
    default:
      return state
  }
}

export default credentials
