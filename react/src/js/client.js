import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import thunkMiddleware from 'redux-thunk';
import todoApp from './reducers';
import { fetchToken } from './actions';
import { fetchRoutines } from './actions/routines';
import { fetchRoutinedays } from './actions/routinedays';
import api from './middleware/api';
import Root from './components/Root';

const store = createStore(
  todoApp,
  applyMiddleware(
    thunkMiddleware,
    api,
  )
);

render(
  <Root store={store} />,
  document.getElementById('root')
);

store.dispatch(fetchToken('guy@test.com', 'passward'))
