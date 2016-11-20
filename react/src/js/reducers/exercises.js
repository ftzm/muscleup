const exercises = (state = {
  isFetching: false,
  exercises: []
}, action) => {
  switch (action.type) {
    case 'EXERCISES_REQUEST':
      return Object.assign({}, state, {
        isFetching: true
      })
    case 'EXERCISES_SUCCESS':
      return Object.assign({}, state, {
        isFetching: false,
        exercises: action.response
      })
    default:
      return state
  }
}

export default exercises
