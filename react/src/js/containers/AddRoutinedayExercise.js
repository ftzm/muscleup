import React from 'react'
import {
  connect
} from 'react-redux'

import {
  renameRoutineday
} from '../actions/routines'

class AddRoutinedayExercise extends React.Component {

  prunedExercises() {
    const existingExercises = this.props.rd
      .get('routinedayslots')
      .toArray()
      .map(rds => rds.get('exercise'))
    const pruned = this.props.exercises.toArray()
      .reduce((acc, x) => {
        if (existingExercises.indexOf(x.get('id')) == -1) {
          return acc.concat(x)
        } else {
          return acc
        }
      }, [])
    return pruned
  }

  render() {
    this.prunedExercises()
    return (
      <div>
         Add Exercise: 
            <select>
                {this.prunedExercises().map(e => 
                   <option key={e.get('id')}>{e.get('name')}</option>
                )}
            </select>
      </div>
    )
  }
}

AddRoutinedayExercise = connect()(AddRoutinedayExercise)

export default AddRoutinedayExercise
