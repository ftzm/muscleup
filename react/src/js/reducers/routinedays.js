import { Map } from 'immutable'

const routinedaysMap = (objectArray, id) =>
      Map(objectArray.map(routineday => [routineday.id, Map(routineday).set('routine', id)]))

const routinedays = (state = Map({
  isFetching: false,
  routinedays: Map(),
}), action) => {
  switch (action.type) {
    case 'ROUTINEDAYS_REQUEST':
      return state.set('isFetching', true)
    case 'ROUTINEDAYS_REQUEST_FAILURE':
      return state.set('isFetching', false)
    case 'ROUTINEDAYS_SUCCESS':
      return state.set('isFetching', false)
        .set('routinedays', routinedaysMap(action.response, action.routine))
    case 'ROUTINEDAY_ADDED':
      return state.setIn(['routinedays', action.response.id],
                         Map(action.response))
    case 'ROUTINEDAY_RENAMED':
      return state.setIn(['routinedays', action.response.id, 'name'],
                         action.response.name)
    case 'ROUTINEDAY_DELETED':
      return state.deleteIn(['routinedays', action.id])
    default:
      return state
  }
}

export default routinedays
