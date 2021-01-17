import React from "react"
import './App.css';

import {
  BrowserRouter as Router,
  Route,
  Switch,
  Link,
  Redirect
} from "react-router-dom";



//importing different pages
import LessThan4YearsPage from './LessThan4YearsPage/LessThan4YearsPage'
import HomePage from "./HomePage";
import Form_Main from './components/form_main';
import MoreThan4YearsPage from './MoreThan4YearsPage/MoreThan4YearsPage'

function App() {

  return (
    <div className="App">
      <Router>
        <Switch>
          <Route exact path="/">
            <HomePage />
          </Route>
          <Route path="/less_than_3_years">
            <LessThan4YearsPage />
          </Route>
          <Route path="/more_than_3_years">
            <MoreThan4YearsPage />
          </Route>
        </Switch>
      </Router>

    </div>
  );
}

export default App;
