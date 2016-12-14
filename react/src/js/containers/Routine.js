import { connect } from 'react-redux'
import { fetchRoutinesIfNeeded, deleteRoutine, deleteRoutineday, renameRoutine } from '../actions/routines'
import RoutinePage from '../components/RoutinePage'

const mapStateToProps = (state) => {
  return {
    exercises: state.exercises.get('exercises'),
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    maybeFetchRoutines: () => dispatch(fetchRoutinesIfNeeded()),
    delete: (id) => dispatch(deleteRoutine(id)),
    deleteRoutineday: (r, rd) => dispatch(deleteRoutineday(r, rd)),
    rename: (name) => dispatch(renameRoutine(name)),
  }
}

const Routine = connect(
  mapStateToProps,
  mapDispatchToProps
)(RoutinePage)

export default Routine
