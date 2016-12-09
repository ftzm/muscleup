import React from 'react'
import { connect } from 'react-redux'
import { renameRoutine } from '../actions/routines'

let RoutineRename = ({ dispatch, id }) => {
  let name

  return (
    <div>
    <form onSubmit={e => {
      e.preventDefault()
      if (!name.value.trim()) {
        return
      }

      dispatch(renameRoutine(id, name.value))
      name.value = ''
    }}>

    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
    <input class="mdl-textfield__input" type="text" id="sample3"
    ref={node => {
      name = node
    }} />

    <label class="mdl-textfield__label" for="sample3">Text...</label>
    </div>
    </form>
    </div>
  )
}

RoutineRename = connect()(RoutineRename)

export default RoutineRename
