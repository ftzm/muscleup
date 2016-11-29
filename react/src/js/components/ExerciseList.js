import React, { PropTypes } from 'react'
import ExerciseAdd from '../containers/ExerciseAdd'
import ExerciseRename from '../containers/ExerciseRename'
import { List, ListItem, ListItemContent, ListItemAction } from 'react-mdl/lib/List';
import { Grid, Cell } from 'react-mdl/lib/Grid';

const ExerciseList = ({ exercises, onFetchClick, onExerciseClick }) => (
  <div>
    <div onClick={() => onFetchClick()} >
      <span >fetchem</span>
    </div>
    <Grid className="test">
      <Cell col={4}>
        <List>
          {exercises.map((ex) =>
            <ListItem key={ex.id}>
              <ListItemContent icon="fitness_center">{ex.name}</ListItemContent>
              <ListItemAction>
                <div onClick={
                  () => {
                    console.log('divclick');
                    console.log(ex.id);
                    onExerciseClick(ex.id)
                  }
                }>
                  <a href="#"><i class="material-icons">delete</i></a>
                </div>
              </ListItemAction>
              <ExerciseRename id={ex.id} />
            </ListItem>)
          }
        </List>
      </Cell>
      <Cell col={4}>col 2</Cell>
      <Cell col={4}>col 3</Cell>
    </Grid>
    <ExerciseAdd/>
  </div>
)

export default ExerciseList
