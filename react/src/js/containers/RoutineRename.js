import React from 'react'
import { connect } from 'react-redux'
import { renameRoutine } from '../actions/routines'

class RoutineRename extends React.Component {
  constructor(props) {
    super(props)
    this.state = { activeTab: 0 };
  }

  componentDidMount() {
    var dialog = document.querySelector('dialog');
    var showDialogButton = document.querySelector('#show-dialog');
    if (! dialog.showModal) {
      dialogPolyfill.registerDialog(dialog);
    }
    showDialogButton.addEventListener('click', function() {
      dialog.showModal();
    });
    dialog.querySelector('.close').addEventListener('click', function() {
      dialog.close();
    });
    this.dialog = document.querySelector('dialog');
  }

  render() {
    let name
    return (
        <div>
               <div id="show-dialog"><i className="material-icons">edit</i></div>
  <dialog className="mdl-dialog">
    <h4 className="mdl-dialog__title">Rename</h4>
    <div className="mdl-dialog__content">
        <form onSubmit={e => {
        this.dialog.close()
        e.preventDefault()
        if (!name.value.trim()) {
            return
        }

        this.props.dispatch(renameRoutine(this.props.id, name.value))
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
    </div>
    <div className="mdl-dialog__actions">
      <button type="button" className="mdl-button">Submit</button>
      <button type="button" className="mdl-button close">Cancel</button>
    </div>
  </dialog>
        </div>
    )
  }
}

RoutineRename = connect()(RoutineRename)

export default RoutineRename
