import React, { PropTypes } from 'react'

const ExerciseList = ({ exercises, onFetchClick }) => (
  <div onClick={() => onFetchClick()} >
  <span >fetchem</span>
  <ul>
  {exercises.map((ex) => <li key={ex.id}>{ex.name}</li>)}
  </ul>
  </div>
)

export default ExerciseList
