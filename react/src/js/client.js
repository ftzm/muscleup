import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import thunkMiddleware from 'redux-thunk';
import todoApp from './reducers';
import { fetchExercises, fetchToken } from './actions';
import api from './middleware/api';
import Root from './components/Root';

const store = createStore(
  todoApp,
  applyMiddleware(
    thunkMiddleware,
    api
  )
);

render(
  <Root store={store} />,
  document.getElementById('root')
);
