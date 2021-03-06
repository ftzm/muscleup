import React, { Component, PropTypes } from 'react'
import * as IP from 'react-immutable-proptypes'
import ExerciseAdd from '../containers/ExerciseAdd'
import ExerciseRename from '../containers/ExerciseRename'
import { List, ListItem, ListItemContent, ListItemAction } from 'react-mdl/lib/List';
import { Grid, Cell } from 'react-mdl/lib/Grid';
import Spinner from 'react-mdl/lib/Spinner';

class ExerciseList extends Component {

  componentDidMount() {
    this.props.maybeFetchExercises()
  }

  render() {
    return (
      <div>
        <Grid className="test">
          <Cell col={4}>
            { this.props.exercises.get('isFetching') ? <Spinner/> :
              <List>
                {this.props.exercises.get('exercises').valueSeq().map((ex) =>
                  <ListItem key={ex.get('id')}>
                      <ListItemContent icon="fitness_center">
                          {ex.get('id')}
                          {ex.get('name')}
                      </ListItemContent>
                      <ListItemAction>
                        <div onClick={
                           () => {
                             this.props.onExerciseClick(ex.get('id'))
                           }
                      }>
                        <a href="#"><i className="material-icons">delete</i></a>
                      </div>
                    </ListItemAction>
                    <ExerciseRename id={ex.get('id')} />
                  </ListItem>)
                }
                <ListItem>
                  <ListItemContent icon="add">
                    <ExerciseAdd/>
                  </ListItemContent>
                </ListItem>
              </List>
            }
          </Cell>
          <Cell col={4}>Second column</Cell>
          <Cell col={4}>Third column</Cell>
        </Grid>
      </div>
    )
  }
}

ExerciseList.propTypes = {
    maybeFetchExercises: PropTypes.func,
    onExerciseClick: PropTypes.func,
    exercises: IP.map
}

export default ExerciseList
