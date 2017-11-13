const initialState = {
  isAuthenticated: false,
  token: null,
  loading: true
};

function auth(state = initialState, action = {}) {
  switch (action.type) {
    case 'LOGIN':
      return {
        ...state,
        loading: true
      };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        loading: false,
        token: action.payload.token,
        isAuthenticated: true
      };
    case 'LOGIN_FAIL':
      return {
        ...state,
        token: null,
        loading: false,
        error: action.error
      };
    case 'LOGOUT':
      return {
        ...state,
        loading: true
      };
    case 'LOGOUT_SUCCESS':
      return {
        ...state,
        loading: false,
        token: null,
        isAuthenticated: false
      };
    case 'LOGOUT_FAIL':
      return {
        ...state,
        loading: false,
        error: action.error
      };
    default:
      return state;
  }
}

export default auth;
