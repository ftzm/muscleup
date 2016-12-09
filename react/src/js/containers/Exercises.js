import { connect } from 'react-redux'
import { Map } from 'immutable'
import { fetchExercisesIfNeeded, deleteExercise, renameExercise } from '../actions/exercises'
import ExerciseList from '../components/ExerciseList'

const mapStateToProps = (state) => {
  return {
    exercises: state.exercises,
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    maybeFetchExercises: () => dispatch(fetchExercisesIfNeeded()),
    onExerciseClick: (id) => dispatch(deleteExercise(id)),
    rename: (name) => dispatch(rename(name)),
  }
}

const Exercises = connect(
  mapStateToProps,
  mapDispatchToProps
)(ExerciseList)

export default Exercises
