import logo from './logo.svg';
import './App.css';
import { Component } from 'react';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = { apiResponse: "" };
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <p>
            {this.state.apiResponse}
          </p>
        </header>
      </div>
    );
  }
}

export default App;
