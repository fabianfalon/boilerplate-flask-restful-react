import * as axios from 'axios';
import cookie from 'react-cookies';

export function loadBooks(pages, limit, sortField, sortDirection) {
  return async dispatch => {
    const token = cookie.load('token');
    axios
      .get(`http://localhost:5000/api/v1/books`, {
        headers: {
          Authorization: `Bearer ${token}`
        },
        params: {
          pages,
          limit,
          sortField,
          sortDirection
        }
      })
      .then(res => {
        dispatch({
          type: 'LOAD_BOOKS_SUCCESS',
          payload: res.data
        });
      })
      .catch(err => {
        dispatch({
          type: 'LOAD_BOOKS_FAIL',
          payload: err
        });
      });
  };
}

export function addBooks(data) {
  return async dispatch => {
    const token = cookie.load('token');
    axios.defaults.headers.common.Authorization = `Bearer ${token}`;
    axios
      .post(`http://localhost:5000/api/v1/books`, {
        ...data
      })
      .then(res => {
        dispatch({
          type: 'ADD_BOOK_SUCCESS',
          payload: res.data
        });
      })
      .catch(err => {
        dispatch({
          type: 'ADD_BOOK_FAIL',
          payload: err
        });
      });
  };
}

export default {
  loadBooks,
  addBooks
};
