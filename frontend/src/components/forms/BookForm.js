import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';

import FormErrors from './FormErrors'

class BookForm extends Component {

  constructor (props) {
    super(props)

    this.state = {
      formData: {
        name: '',
        description: '',
        autor: '',
      },
      formRules: [
        {
          id: 1,
          field: 'name',
          name: 'name is required.',
          valid: false
        },
        {
          id: 2,
          field: 'description',
          name: 'description is required.',
          valid: false
        },
        {
          id: 3,
          field: 'autor',
          name: 'autor is required.',
          valid: false
        }
      ],
      valid: false
    }
    this.handleLoginFormSubmit = this.handleLoginFormSubmit.bind(this);
  }

  componentDidMount() {
    this.clearForm();
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.formType !== nextProps.formType) {
      this.clearForm();
      this.initRules();
    }
  }

  clearForm() {
    this.setState({
      formData: {email: '', password: ''}
    });
  }

  initRules() {
    const rules = this.state.formRules;
    for (const rule of rules) {
      rule.valid = false;
    }
    this.setState({formRules: rules})
  }

  handleFormChange(event) {
    const obj = this.state.formData;
    obj[event.target.name] = event.target.value;
    this.setState(obj);
    this.validateForm()
  }

  allTrue() {
    for (const rule of this.state.formRules) {
      if (!rule.valid) return false;
    }
    return true;
  }

  validateForm() {
    const rules = this.state.formRules;
    const formData = this.state.formData;
    this.setState({valid: false});
    for (const rule of rules) {
      rule.valid = false;
    }
    if (formData.name && formData.name.length > 0) {
      rules[0].valid = true;
    }
    if (formData.description && formData.description.length > 0) {
      rules[1].valid = true;
    }
    if (formData.autor && formData.autor.length > 0) {
      rules[2].valid = true;
    }    
    this.setState({formRules: rules})
    if (this.allTrue()) this.setState({valid: true});
  }

  handleLoginFormSubmit(event) {
    const data = {
      name: this.state.formData.name,
      description: this.state.formData.description,
      autor: this.state.formData.autor
    }
    event.preventDefault();
    this.props.addBook(data);
    this.clearForm();
    window.location.replace('http://localhost:3000');
  }
  render() {
    if (this.props.isAuthenticated) {
      return <Redirect to='/' />;
    }
    return (
      <div>
        <h1>Login</h1>
        <hr/><br/>
        <FormErrors
          formRules={this.state.formRules}
        />
        <form onSubmit={(event) => this.handleLoginFormSubmit(event)}>
          <div className="form-group">
            <input
              name="name"
              className="form-control input-md"
              type="text"
              placeholder="Enter an name"
              required
              value={this.state.formData.name}
              onChange={this.handleFormChange.bind(this)}
            />
          </div>
          <div className="form-group">
            <input
              name="description"
              className="form-control input-md"
              type="text"
              placeholder="Enter a description"
              required
              value={this.state.formData.description}
              onChange={this.handleFormChange.bind(this)}
            />
          </div>
          <div className="form-group">
            <input
              name="autor"
              className="form-control input-md"
              type="text"
              placeholder="Enter a autor"
              required
              value={this.state.formData.autor}
              onChange={this.handleFormChange.bind(this)}
            />
          </div>
          <input
            type="submit"
            className="btn btn-primary btn-md"
            value="Submit"
          />
        </form>
      </div>
    )
  }
}

export default BookForm