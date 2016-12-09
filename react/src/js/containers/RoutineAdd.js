import React from 'react'
import { connect } from 'react-redux'
import { addRoutine } from '../actions/routines'

let RoutineAdd = ({ dispatch }) => {
  let name
  let length
  let position

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

      dispatch(addRoutine(name.value, length.value, position.value))
      name.value = ''
      length.value = ''
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
    <input class="mdl-textfield__input" type="text" id="sample2"
    ref={node => {
      length = node
    }} />
    <label class="mdl-textfield__label" for="sample2">Text...</label>
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

RoutineAdd = connect()(RoutineAdd)

export default RoutineAdd
