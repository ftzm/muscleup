import React, { PropTypes } from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux';
import { Router, Route, browserHistory, Link } from 'react-router';
import App from './App';
import Footer from './Footer';
import Creds from '../containers/Creds'
import Exercises from '../containers/Exercises'
import Routines from '../containers/Routines'

const drawerCheck = () => {
  var l = document.querySelector('.mdl-layout').MaterialLayout
  if (l.drawer_.classList.contains(l.CssClasses_.IS_DRAWER_OPEN)) {
    l.toggleDrawer()
  }
}

const Root = ({ store }) => (
  <Provider store={store}>
    <Router history={browserHistory} onUpdate={drawerCheck}>
      <Route path="/" component={App}>
        <Route path="/exercises" component={Exercises}/>
        <Route path="/routines" component={Routines}/>
        <Route path="/login" component={Creds}/>
      </Route>
    </Router>
  </Provider>
);

Root.propTypes = {
  store: PropTypes.object.isRequired,
};

export default Root;
