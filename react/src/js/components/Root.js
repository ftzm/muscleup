import React, { PropTypes } from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux';
import { Router, Route, browserHistory, Link } from 'react-router';
import App from './App';
import Footer from './Footer';
import Exercises from '../containers/Exercises'

const Root = ({ store }) => (
  <Provider store={store}>
    <Router history={browserHistory}>
      <Route path="/" component={App}>
        <Route path="/exercises" component={Exercises}/>
        <Route path="/footer" component={Footer}/>
      </Route>
    </Router>
  </Provider>
);

Root.propTypes = {
  store: PropTypes.object.isRequired,
};

export default Root;
