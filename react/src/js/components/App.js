import React from 'react'
import { Link } from 'react-router';
import Creds from '../containers/Creds'

const App = ({ children }) => (
  <div>
    <ul role="nav">
      <li><Link to="/exercises">ex</Link></li>
      <li><Link to="/footer">fo</Link></li>
    </ul>
    <Creds/>
    {children}
  </div>
)

export default App
