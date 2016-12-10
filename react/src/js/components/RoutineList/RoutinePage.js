import React from "react";
import {
  List,
  ListItem,
  ListItemContent,
  ListItemAction
} from 'react-mdl/lib/List'
import RoutineRename from '../../containers/RoutineRename'

export default class Header extends React.Component {
  render() {
    return (
      <List>
         <ListItem>
            <ListItemContent>
              Name: {this.props.r.get('name')}
            </ListItemContent>
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
                 <RoutineRename id={this.props.r.get('id')} />
            </ListItemContent>
         </ListItem>
         {this.props.r.get('routinedays').valueSeq().map((rd, i) =>
             <ListItem key={rd.get('id')}>
             <ListItemContent>
                 Name: {rd.get('name')}
             </ListItemContent>
             </ListItem>
         )}
       </List>
    )
  }
}
