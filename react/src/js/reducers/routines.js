import { Map } from 'immutable'

const routinesMap = (objectArray) =>
  Map(objectArray.map(routine => [routine.id, Map(routine)]))

const routines = (state = Map({
  isFetching: false,
  routines: Map(),
}), action) => {
  switch (action.type) {
    case 'ROUTINES_REQUEST':
      return state.set('isFetching', true)
    case 'ROUTINES_REQUEST_FAILURE':
      return state.set('isFetching', false)
    case 'ROUTINES_SUCCESS':
      return state.set('isFetching', false)
        .set('routines', routinesMap(action.response))
    case 'ROUTINE_ADDED':
      return state.setIn(['routines', action.response.id],
                         Map(action.response))
    case 'ROUTINE_RENAMED':
      return state.setIn(['routines', action.response.id, 'name'],
                         action.response.name)
    case 'ROUTINE_DELETED':
      return state.deleteIn(['routines', action.id])
    default:
      return state
  }
}

export default routines
