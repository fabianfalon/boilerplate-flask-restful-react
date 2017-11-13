import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';

import App from './App.js';

import { Provider } from 'react-redux';
// import Store from './store';

// const StoreInstance = Store();

// ReactDOM.render((
//   <Router>
//     <App />
//   </Router>
// ), document.getElementById('root'))

import store from './store';

ReactDOM.render(
 <Provider store={store}>
   <Router>
     <App />
   </Router>
 </Provider>,
 document.getElementById('root')
);