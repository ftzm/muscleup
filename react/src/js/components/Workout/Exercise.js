import React from "react";

import Set from "./Set";

export default class Exercise extends React.Component {

  render() {

    var sets = this.props.sets.map((s, i) => <Set s={s} id={this.props.i+"-"+i} key={i} changeCurrentSet={this.props.changeCurrentSet} currentSet={this.props.currentSet} />);

    return (
      <div>
        {this.props.i}: {this.props.name}
        <br/>
        {sets}
        <br/>
      </div>
    );
  }
}
