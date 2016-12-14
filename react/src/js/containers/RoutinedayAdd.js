import React from 'react'
import { connect } from 'react-redux'
import { addRoutineday } from '../actions/routines'

const mapStateToProps = (state, ownProps) => {
  return {
      routineId: ownProps.routineId
  }
}

let RoutinedayAdd = ({ dispatch, routineId }) => {
      console.log(routineId)
  let name
  let position

  return (
    <div>
    <form onSubmit={e => {
      e.preventDefault()

      if (!name.value.trim()) {
        return
      }

      if (!position.value.trim()) {
          return
      }

      dispatch(addRoutineday(name.value, routineId, position.value))
      name.value = ''
      position.value = ''
    }}>

    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
      <input class="mdl-textfield__input" type="text" id="sample1"
      ref={node => {
        name = node
      }} />

      <label class="mdl-textfield__label" for="sample1">Text...</label>

    </div>

    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
    <input class="mdl-textfield__input" type="text" id="sample3"
    ref={node => {
      position = node
    }} />

    <label class="mdl-textfield__label" for="sample3">Text...</label>
    </div>

    <input type="submit" value="Submit"/>

    </form>
    </div>
  )
}

RoutinedayAdd = connect(
  mapStateToProps
)(RoutinedayAdd)

export default RoutinedayAdd
