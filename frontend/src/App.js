import React, { Component, Suspense } from 'react'
import { HashRouter, Route, Navigate, Routes } from 'react-router-dom'
import './scss/style.scss'
import Private from './components/Private'

const loading = (
  <div className="pt-3 text-center">
    <div className="sk-spinner sk-spinner-pulse"></div>
  </div>
)

// Containers
const DefaultLayout = React.lazy(() => import('./layout/DefaultLayout'))

// Pages
const Login = React.lazy(() => import('./views/pages/login/Login'))

class App extends Component {
  render() {
    return (
      <HashRouter>
        <Suspense fallback={loading}>
          <Routes>
            <Route exact path="/login" name="Login Page" element={<Login />} />
            <Route path="*" name="Home" element={<Private Component={DefaultLayout} />} />
          </Routes>
        </Suspense>
      </HashRouter>
    )
  }
}

export default App
