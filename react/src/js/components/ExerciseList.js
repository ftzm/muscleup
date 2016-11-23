import React, { PropTypes } from 'react'
import ExerciseAdd from '../containers/ExerciseAdd'

const ExerciseList = ({ exercises, onFetchClick }) => (
  <div onClick={() => onFetchClick()} >
  <span >fetchem</span>
  <ul>
  {exercises.map((ex) => <li key={ex.id}>{ex.name}</li>)}
  </ul>
  <ExerciseAdd/>
  </div>
)

export default ExerciseList
