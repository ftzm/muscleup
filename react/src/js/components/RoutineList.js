import React, { Component, PropTypes } from 'react'
import RoutineAdd from '../containers/RoutineAdd'
import RoutineRename from '../containers/RoutineRename'
import { List, ListItem, ListItemContent, ListItemAction } from 'react-mdl/lib/List'
import { Grid, Cell } from 'react-mdl/lib/Grid'
import Spinner from 'react-mdl/lib/Spinner'

class RoutineList extends Component {

  componentDidMount() {
    this.props.maybeFetchRoutines()
  }

  render() {
    return (
      <div>
        <Grid className="test">
          <Cell col={4}>
            { this.props.routines.get('isFetching') ? <Spinner/> :
              <List>
                {this.props.routines.get('routines').valueSeq().map((ex) =>
                  <ListItem key={ex.get('id')}>
                    <ListItemContent icon="fitness_center">
                      {ex.get('id')}<br/>
                      {ex.get('name')}<br/>
                      {ex.get('cycle_length')}<br/>
                      {ex.get('cycle_position')}<br/>
                      {ex.get('routinedays')}<br/>
                    <div onClick={() => {
                      this.props.fetchRoutinedays(ex.get('id'))
                    }}>fetch</div>
                    </ListItemContent>
                    <ListItemAction>
                      <div onClick={
                        () => {
                          onRoutineClick(ex.get('id'))
                        }
                      }>
                        <a href="#"><i class="material-icons">delete</i></a>
                      </div>
                    </ListItemAction>
                    <RoutineRename id={ex.get('id')} />
                  </ListItem>)
                }
                <ListItem>
                  <ListItemContent icon="add">
                    <RoutineAdd/>
                  </ListItemContent>
                </ListItem>
              </List>
            }
        
          </Cell>
          <Cell col={4}>
            <div>
              <span>Routinedays</span>
        { this.props.routinedays.get('routinedays').valueSeq().map(
            (rd) => <span>{rd.get('name')}</span>
        )}
            </div>
          </Cell>
          <Cell col={4}>Third column</Cell>
        </Grid>
      </div>
    )
  }
}

export default RoutineList
