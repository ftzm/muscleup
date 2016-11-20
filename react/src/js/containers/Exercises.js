import { connect } from 'react-redux'
import { fetchExercises } from '../actions/exercises'
import ExerciseList from '../components/ExerciseList'

const mapStateToProps = (state) => {
  return {
    exercises: state.exercises.exercises
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    onFetchClick: () => dispatch(fetchExercises())
  }
}

const Exercises = connect(
  mapStateToProps,
  mapDispatchToProps
)(ExerciseList)

export default Exercises
