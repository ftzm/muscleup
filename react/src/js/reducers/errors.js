const errors = (state = {
  message: '',
  active: false,
}, action) => {
  switch (action.type) {
    case 'ERROR_NEW':
      return Object.assign({}, state, {
        active: true,
        message: action.message,
      })
    case 'ERROR_TIMEOUT':
      return Object.assign({}, state, {
        active: false,
        message: '',
      })
    default:
      return state
  }
}

export default errors
