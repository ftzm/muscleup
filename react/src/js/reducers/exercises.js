import { Map } from 'immutable'

const exercisesMap = (objectArray) =>
  Map(objectArray.map(exercise => [exercise.id, Map(exercise)]))

const exercises = (state = Map({
  isFetching: false,
  exercises: Map(),
}), action) => {
  switch (action.type) {
    case 'EXERCISES_REQUEST':
      return state.set('isFetching', true)
    case 'EXERCISES_REQUEST_FAILURE':
      return state.set('isFetching', false)
    case 'EXERCISES_SUCCESS':
      return state.set('isFetching', false)
        .set('exercises', exercisesMap(action.response))
    case 'EXERCISE_ADDED':
      return state.setIn(['exercises', action.response.id],
                         Map(action.response))
    case 'EXERCISE_RENAMED':
      return state.setIn(['exercises', action.response.id, 'name'],
                         action.response.name)
    case 'EXERCISE_DELETED':
      return state.deleteIn(['exercises', action.id])
    default:
      return state
  }
}

export default exercises
