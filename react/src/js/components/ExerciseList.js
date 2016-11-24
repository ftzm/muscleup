import React, { PropTypes } from 'react'
import ExerciseAdd from '../containers/ExerciseAdd'

const ExerciseList = ({ exercises, onFetchClick, onExerciseClick }) => (
  <div onClick={() => onFetchClick()} >
  <span >fetchem</span>
  <ul>
  {exercises.map((ex) => <li key={ex.id}><div onClick={() => {console.log('divclick'); console.log(ex.id); onExerciseClick(ex.id)}}>{ex.name} {ex.id}</div></li>)}
  </ul>
  <ExerciseAdd/>
  </div>
)

export default ExerciseList
