import React from "react";
import {
  List,
  ListItem,
  ListItemContent,
  ListItemAction
} from 'react-mdl/lib/List'

import RoutineRename from '../containers/RoutineRename'
import RoutinedayRename from '../containers/RoutinedayRename'
import RoutinedayAdd from '../containers/RoutinedayAdd'
import AddRoutinedayExercise from '../containers/AddRoutinedayExercise'

import { renameRoutineday } from '../actions/routines'


export default class Header extends React.Component {

  render() {
    return (
      <div>
      <List>
         <ListItem>
            <ListItemContent>
              Name: {this.props.r.get('name')}
            </ListItemContent>
             <ListItemAction>
                 <RoutineRename id={this.props.r.get('id')} />
             </ListItemAction>
             <ListItemAction>
             <div onClick={
                 () => {
                 this.props.delete(this.props.r.get('id'))
                 }
             }>

                 <a href="#"><i class="material-icons">delete</i></a>
             </div>
             </ListItemAction>
         </ListItem>
         <ListItem>
            <ListItemContent>
                Cycle Length: {this.props.r.get('cycle_length')}
                Cycle position: {this.props.r.get('cycle_position')}
            </ListItemContent>
         </ListItem>
        </List>
        <h4>Scheduled Days</h4>
        <List>
         {this.props.r.get('routinedays').valueSeq().map((rd, i) =>
        <div key={rd.get('id')}>
             <ListItem key={rd.get('id')}>
             <ListItemContent>
                 Name: {rd.get('name')}<br/>
                 Exercises:<br/>
             </ListItemContent>
             <ListItemAction>
                 <RoutinedayRename 
                    func={(name) =>
                        renameRoutineday(
                            rd.get('routine'),
                            rd.get('id'),
                            name
                        )
                    }
                 />
             </ListItemAction>
             <ListItemAction>
             <div onClick={
                 () => {
                 this.props.deleteRoutineday(rd.get('routine'), rd.get('id'))
                 }
             }>

                 <a href="#"><i class="material-icons">delete</i></a>
             </div>
             </ListItemAction>
             </ListItem>
             <ListItem>
             <ListItemContent>
                 <List>
                      {rd.get('routinedayslots').valueSeq().map((rds) =>(
                      <ListItem key={rds.get('id')}>
                          <ListItemContent>
                              {this.props.exercises.getIn([(rds.get('exercise')
                                 .toString()), 'name'])}
                          </ListItemContent>
                      </ListItem>
                      ))}
                      <ListItem>
                          <ListItemContent>
                              <AddRoutinedayExercise
                                  rd={rd}
                                  exercises={this.props.exercises}
                              />
                          </ListItemContent>
                      </ListItem>
                 </List>
             </ListItemContent>
             </ListItem>
             </div>
         )}
         <ListItem>
            <ListItemContent>
                <RoutinedayAdd
                    routineId={this.props.r.get('id')}
                />
            </ListItemContent>
         </ListItem>
       </List>
     </div>
    )
  }
}
