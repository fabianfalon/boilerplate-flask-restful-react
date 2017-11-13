import React, { Component } from 'react';
import { Route, Switch, withRouter } from 'react-router-dom';
import BooksList from './components/Books/BooksList';
import About from './components/About/About';
import NavBar from './components/NavBar';
import Logout from './components/Logout';
import BookForm from './components/forms/BookForm';
import LoginForm from './components/forms/LoginForm';
import cookie from 'react-cookies';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import * as bookActions from './actions/books';
import * as authActions from './actions/auth';

class App extends Component {
  constructor() {
    super();
    this.settingStates = this.settingStates.bind(this);
    this.state = {
      pages: 0,
      limit: 10,
      sortField: 'name',
      sortDirection: 'asc',
      title: 'Books apps',
      // isAuthenticated: true
    };
  }

  componentWillMount() {
    this.props.actions.loadBooks(
      this.state.pages,
      this.state.limit,
      this.state.sortField,
      this.state.sortDirection
    );
  }

  settingStates(page, limit, sortField, sortDirection) {
    this.setState({
      ...this.state,
      page: page,
      limit: limit,
      sortField: sortField,
      sortDirection: sortDirection
    });
  }

  render() {
    const isAuthenticated = cookie.load('isAuthenticated');
    return (
      <div>
        <NavBar
          title={this.state.title}
          isAuthenticated={isAuthenticated}
          logo
        />
        <div className="container-fluid">
          <div className="col-lg-12">
            <div className="col-md-12">
              <br />
              <Switch>
                <Route
                  exact
                  path="/"
                  render={() => (
                    <BooksList
                      books={this.props.books.books}
                      pages={this.props.books.pages}
                      getBooks={this.props.actions.loadBooks}
                      settingStates={this.settingStates}
                    />
                  )}
                />
                <Route
                  exact
                  path="/new"
                  render={() => (
                    <BookForm addBook={this.props.actions.addBooks} />
                  )}
                />
                <Route path="/about" component={About} />
                <Route
                  path="/logout"
                  render={() => (
                    <Logout logoutUser={this.props.auth.logoutUser} />
                  )}
                />
                <Route
                  path="/login"
                  render={() => (
                    <LoginForm
                      isAuthenticated={isAuthenticated}
                      loginUser={this.props.auth.loginUser}
                    />
                  )}
                />
                )} />
              </Switch>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

function mapStateToProps(state, props) {
  return {
    books: state.books,
    auth: state.auth
  };
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(bookActions, dispatch),
    auth: bindActionCreators(authActions, dispatch)
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(App));
