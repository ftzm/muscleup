import React from 'react'
import ReactDOM from 'react-dom'
import {
  connect
} from 'react-redux'

import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions
} from 'react-mdl'
import Button from 'react-mdl/lib/Button'

import { renameRoutineday } from '../actions/routines'

class RoutinedayRename extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.handleOpenDialog = this.handleOpenDialog.bind(this);
    this.handleCloseDialog = this.handleCloseDialog.bind(this);
  }

  handleOpenDialog() {
    this.setState({
      openDialog: true
    });
  }

  handleCloseDialog() {
    this.setState({
      openDialog: false
    });
  }

  componentDidMount() {
    const dialog = ReactDOM.findDOMNode(this.dialog);
    if (!dialog.showModal) {
      window.dialogPolyfill.registerDialog(dialog);
    }
  }

  render() {
    let name
    return (
      <div>


<div>
        <Dialog open={this.state.openDialog} ref={node => {this.dialog = node}}>
          <DialogTitle>Rename</DialogTitle>
          <DialogContent>
        <form onSubmit={e => {
        this.handleCloseDialog()
        e.preventDefault()
        if (!name.value.trim()) {
            return
        }


        this.props.dispatch(this.props.func(name.value))
        name.value = ''
        }}>

        <div className="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
        <input className="mdl-textfield__input" type="text" id="sample3"
        ref={node => {
        name = node
        }} />

        <label className="mdl-textfield__label" htmlFor="sample3">Text...</label>
        </div>
        </form>
          </DialogContent>
          <DialogActions>
            <Button type='button'>Agree</Button>
            <Button type='button' onClick={this.handleCloseDialog}>Disagree</Button>
          </DialogActions>
        </Dialog>
      </div>


        <div onClick={() => this.handleOpenDialog()}><i className="material-icons">edit</i></div>
        </div>
    )
  }
}

RoutinedayRename = connect()(RoutinedayRename)

export default RoutinedayRename
