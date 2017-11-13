import * as axios from 'axios';
import cookie from 'react-cookies';
import _ from 'lodash';

export function loginUser(email, password) {
  return async (dispatch) => {
    axios.post(`http://localhost:5000/api/v1/auth`, {
      email,
      password
    })
    .then(res => {
      if (res.data.token && res.data.token !== 'undefined') {
        cookie.save('token', res.data.token);
        cookie.save('isAuthenticated', true);
        dispatch({
          type: 'LOGIN_SUCCESS',
          payload: res.data
        });
      } else {
        console.log('to dispatch submission ')
      }
    })
    .catch(err => {
      console.log(err);
    });
  }
}

export function logoutUser(data) {
  cookie.remove('token');
  cookie.remove('isAuthenticated');
  return {
    type: 'LOGOUT_SUCCESS'
  }
}


export default {
  loginUser,
  logoutUser
};

