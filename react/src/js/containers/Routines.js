import { connect } from 'react-redux'
import { fetchRoutinesIfNeeded, deleteRoutine, renameRoutine } from '../actions/routines'
import { fetchRoutinedays } from '../actions/routinedays'
import RoutineList from '../components/RoutineList'

const mapStateToProps = (state) => {
  return {
    routines: state.routines,
    routinesSorted: state.routines.get('routines')
      .valueSeq()
      .sort((a, b) => a.get('id') - b.get('id'))
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    maybeFetchRoutines: () => dispatch(fetchRoutinesIfNeeded()),
    delete: (id) => dispatch(deleteRoutine(id)),
    rename: (name) => dispatch(renameRoutine(name)),
    fetchRoutinedays: (id) => dispatch(fetchRoutinedays(id))
  }
}

const Routines = connect(
  mapStateToProps,
  mapDispatchToProps
)(RoutineList)

export default Routines
