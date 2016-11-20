import React from "react";

import Footer from "./Footer";
import NowSet from "./NowSet";
import Header from "./Header";
import Exercise from "./Workout/Exercise";

  var exercises = [
    {
      name: 'Bench',
      sets: [
        {weight: 10, reps: 8},
        {weight: 10, reps: 7},
        {weight: 10, reps: 6}
      ]
    },
    {
      name: 'OHP',
      sets: [
        {weight: 10, reps: 8},
        {weight: 10, reps: 7},
        {weight: 10, reps: 6}
      ]
    },
    {
      name: 'Dead',
      sets: [
        {weight: 10, reps: 8},
        {weight: 10, reps: 7},
        {weight: 10, reps: 6}
      ]
    }
  ]

export default class Workout extends React.Component {

  constructor() {
    super();
    this.state = {
      title: "Welcome!!!",
      number: 1001,
      currentSet: "None",
      exercises: exercises,
    };
  }

  changeCurrentSet = (currentSet) => {
    this.setState({currentSet});
  }

  render() {

    var exs = this.state.exercises.map((ex, i) => <Exercise name={ex.name} sets={ex.sets} i={i} key={i} changeCurrentSet={this.changeCurrentSet} currentSet={this.state.currentSet} />);


    return (
      <div>
        <NowSet set={this.state.currentSet} />
        <br/>
        {exs}
      </div>
    );
  }
}
