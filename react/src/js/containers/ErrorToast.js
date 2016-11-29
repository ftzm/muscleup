import React from 'react';
import { connect } from 'react-redux'
import Snackbar from 'react-mdl/lib/Snackbar';
import { errorTimeout } from '../actions'

const mapStateToProps = (state) => ({
  errors: state.errors,
})

const mapDispatchToProps = (dispatch) => ({
  errorTimeout: (message) => dispatch(errorTimeout(message)),
})

const ErrorToastRaw = ({ errors, errorTimeout }) => (
  <div>
  <Snackbar
  active={errors.active}
  onTimeout={errorTimeout}>
  {errors.message}
  </Snackbar>
  </div>
);

const ErrorToast = connect(
  mapStateToProps,
  mapDispatchToProps
)(ErrorToastRaw)

export default ErrorToast;
