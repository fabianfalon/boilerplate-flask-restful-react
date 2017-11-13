import React, { Component } from 'react';
import {Button} from 'react-bootstrap';

export default class Actions extends Component {

  static propTypes = {
  }

  constructor(props) {
    super(props);
    this.state = {showModal: false, };
  }



  render() {
    return (
      <div>
        <center>
         <Button id={`dropdown-size-large-${this.props.item.id}`}
            bsStyle={'warning'}>
              <i style={{textShadow: '1px 1px 1px #ccc'}} className="fa fa-pencil fa-1x"></i>
          </Button>
          &nbsp;&nbsp;
          <Button id={`dropdown-size-large-${this.props.item.id}`}
             bsStyle={'danger'}>
              <i style={{textShadow: '1px 1px 1px #ccc'}} className="fa fa-trash fa-1x"></i>
           </Button>
        </center>
      </div>
    );
  }
}