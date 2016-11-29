import React from 'react'
import { connect } from 'react-redux'
import { addExercise } from '../actions/exercises'

let ExerciseAdd = ({ dispatch }) => {
  let name
  let bodyweight

  return (
    <div>
      <form onSubmit={e => {
        e.preventDefault()
        if (!name.value.trim()) {
          return
        }
        {/*if (!bodyweight.value.trim()) {
          return
        }*/}
        dispatch(addExercise(name.value))
        name.value = ''
        bodyweight.value = ''
        }}>
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
          <input class="mdl-textfield__input" type="text" id="sample3"
            ref={node => {
            name = node
          }} />
          {/*<input ref={node => {
            bodyweight = node
          }} />*/}
          <label class="mdl-textfield__label" for="sample3">Text...</label>
        </div>
      </form>
    </div>
  )
}
ExerciseAdd = connect()(ExerciseAdd)

export default ExerciseAdd
