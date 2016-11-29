import React from 'react'
import { connect } from 'react-redux'
import { renameExercise } from '../actions/exercises'

let ExerciseRename = ({ dispatch, id }) => {
  let name

  return (
    <div>
    <form onSubmit={e => {
      e.preventDefault()
      if (!name.value.trim()) {
        return
      }

      dispatch(renameExercise(id, name.value))
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

ExerciseRename = connect()(ExerciseRename)

export default ExerciseRename
