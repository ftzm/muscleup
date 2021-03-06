import React from 'react'
import { Link } from 'react-router';
import Creds from '../containers/Creds'
import ErrorToast from '../containers/ErrorToast'
import { Layout, Header, Drawer, Navigation } from 'react-mdl/lib/Layout';

const App = ({ children }) => (
    <Layout fixedHeader>
      <Header title={<span><span style={{ color: '#ddd' }}>
        Area / </span><strong>MuscleUp</strong></span>}>
      </Header>
      <Drawer title="Title">
        <Navigation>
          <Link to="/exercises">Exercises</Link>
          <Link to="/routines">Routines</Link>
          <Link to="/login">Login</Link>
          <a href="">Link</a>
          <a href="">Link</a>
        </Navigation>
      </Drawer>
      {children}
      <ErrorToast/>
    </Layout>
)

export default App
