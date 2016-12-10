import React, { Component, PropTypes } from 'react'
import RoutineAdd from '../containers/RoutineAdd'
import RoutinePage from '../components/RoutineList/RoutinePage'
import RoutineRename from '../containers/RoutineRename'
import { List, ListItem, ListItemContent, ListItemAction } from 'react-mdl/lib/List'
import { Tabs, Tab } from 'react-mdl/lib/Tabs'
import { Grid, Cell } from 'react-mdl/lib/Grid'
import Spinner from 'react-mdl/lib/Spinner'

class RoutineList extends Component {
  constructor(props) {
    super(props)
    this.state = { activeTab: 0 };
  }

  componentDidMount() {
    this.props.maybeFetchRoutines()
  }

  render() {
    return (
      <div>
        <div className="demo-tabs">
            <Tabs activeTab={this.state.activeTab}
                  onChange={(tabId) => this.setState({ activeTab: tabId })}
                  ripple>
                {this.props.routinesSorted.map((r) =>
                    <Tab key={r.get('id')}>{r.get('name')}</Tab>
                )}

          <Tab>+</Tab>



            </Tabs>
        </div> 
        <Grid className="test">
          <Cell col={3}>
          </Cell>
          <Cell col={6}>
                <section>
                    <div className="content">
                        {this.props.routinesSorted.map((r, i) =>
                            i == this.state.activeTab ? (
                             <RoutinePage delete={this.props.delete} key={r.get('id')} r={r}/>
                            )
                            : ''
                        )}
                        {this.state.activeTab == this.props.routines.get('routines').toArray().length ? (
                           <RoutineAdd/>
                         ) : ''
                        }
                    </div>
                </section>
          </Cell>
          <Cell col={3}>
          </Cell>
        </Grid>
      </div>
    )
  }
}

export default RoutineList
