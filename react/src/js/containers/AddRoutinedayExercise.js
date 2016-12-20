import React from 'react'
import {
  connect
} from 'react-redux'

import {
    addRoutinedayslot
} from '../actions/routines'

class AddRoutinedayExercise extends React.Component {

  prunedExercises() {
    var existingExercises = this.props.rd
      .get('routinedayslots')
      .toArray()
      .map(rds => rds.get('exercise'))
    var pruned = this.props.exercises.toArray()
      .reduce((acc, x) => {
        if (existingExercises.indexOf(x.get('id')) == -1) {
          return acc.concat(x)
        } else {
          return acc
        }
      }, [])
    
    return pruned
  }

    handleChange(event, rd) {
        this.props.dispatch(
            addRoutinedayslot(
                this.props.rd.get('routine'),
                this.props.rd.get('id'),
                event.target.value
            )
        )
    }

  render() {
    this.prunedExercises()
    return (
      <div>
         Add Exercise:
            <select onChange={(event) => this.handleChange(event, this.props.rd)}>
                {this.prunedExercises().map(e =>
                   <option value={e.get('id')} key={e.get('id')}>{e.get('name')}</option>
                )}
            </select>
      </div>
    )
  }
}

AddRoutinedayExercise = connect()(AddRoutinedayExercise)

export default AddRoutinedayExercise
