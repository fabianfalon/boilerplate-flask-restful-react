import books from './books';
import auth from './auth';

import { combineReducers } from 'redux';

const reducer = combineReducers({
  books: books,
  auth: auth
});

export default reducer;
