const initialState = {
  books: [],
  pages: 0,
  total: 0,
  limit: 2,
  loading: true
};

function books(state = initialState, action = {}) {
  switch (action.type) {
    case 'LOAD_BOOKS':
      return {
        ...state,
        loading: true
      };
    case 'LOAD_BOOKS_SUCCESS':
      return {
        ...state,
        loading: false,
        books: action.payload.data,
        pages: action.payload.pages
      };
    case 'LOAD_BOOKS_FAIL':
      return {
        ...state,
        loading: false,
        error: action.error
      };
    case 'ADD_BOOK':
      return {
        ...state,
        loading: true
      };
    case 'ADD_BOOK_SUCCESS':
      return {
        ...state,
        loading: false,
        books: action.payload.data,
        pages: action.payload.pages
      };
    case 'ADD_BOOK_FAIL':
      return {
        ...state,
        loading: false,
        error: action.error
      };
    default:
      return state;
  }
}

export default books;
