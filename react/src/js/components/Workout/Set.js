import React from "react";

export default class Set extends React.Component {

  handleClick(id) {
    this.props.changeCurrentSet(id)
    //this.setState({active: "bg-warning"})
  }

  render() {
    return (
      <div class={ this.props.id === this.props.currentSet ? "bg-warning" : "" }
        onClick={() => this.handleClick(this.props.id)}>
        {this.props.id}: {this.props.s.weight}/
        {this.props.s.reps}
      </div>
    );
  }
}
