import React, { Component } from 'react';
import {
    Link
} from 'react-router-dom';
import Field from './Field';
import ErrorList from './Errors';
import './Register.css';
import {connect} from "react-redux";
import {auth} from '../../actions';


/*
    ButtonModal shows a submit button, but after submission,
    it expands into an informational modal.
*/
class ButtonModal extends Component {
    constructor(props) {
        super(props);
        this.state = {
            expanded: false
        }
    }
    expandDiv(event) {
        console.log(this);
        
    }


    render() {
        return (
            <div className={this.props.expanded
                    ? 'expanded'
                    : ''}>
                {this.props.expanded
                    ? <div className="modal">
                        <h1>Welcome to Kaiketsu!</h1>
                        <p>
                        We created KAIKETSU to allow users like you
                        to set daily goals, and keep track of their
                        progress over time. Goals are categorized into
                        3 types - Health & Wellness, Personal, and Professional.
                        We hope the experience of KAIKETSU motivates you along
                        your journey!</p>
                        <Link to="/dashboard/create-goal/">
                        <button>
                            Create My First Goal
                        </button>
                        
                        </Link>
                    </div>
                    : ''}
                <button className="submit"
                    type="submit"
                    value="submit"
                    onClick={this.expandDiv.bind(this)}
                >Sign Up</button>
            </div>
        );
    }
}



class Register extends Component {
    constructor(props) {
        super(props);
        this.state = {
            toGoalPrompt: false,
            showWelcome: false
        }
        this.registerAccount = this.registerAccount.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
        this.setState({inputField: event.target.value});
    }

    resetForm() {
        this.setState({
            currentField: 0,
            responses: []
        })
    }

    registerAccount(event) {
        event.preventDefault();
        let data  = new FormData(event.target);
        console.log(data.get('username'));
        this.props.register(
            data.get('username'),
            data.get('first_name'),
            data.get('email'),
            data.get('password'))
        .then(() => {
            this.setState((state) => {
                return {
                    showWelcome: true,
                    toGoalPrompt: true
                }
            });
        }).catch((error) => {
            console.log(error);
        });
        
        
    }
    
    render() {

        return (
            <div className="Register">
                <h1>Sign Up</h1>
                <form className="registrationForm" onSubmit={this.registerAccount}>
                    <div className="form-inner">
                        <Field
                            type="text"
                            for="username"
                            field="username"
                            label="Username"
                            placeholder="leajones151"
                        ></Field>
                        <Field
                            type="text"
                            for="first_name"
                            field="first_name"
                            label="First Name"
                            placeholder="Lea"
                        ></Field>
                        <Field
                            type="email"
                            for="email"
                            field="email"
                            label="Email"
                            placeholder="Lea.Jones@email.com"
                        ></Field>
                        <Field
                            type="password"
                            for="password"
                            field="password"
                            label="Password"
                            placeholder="Must have at least 8 characters"
                        ></Field>
                        
                        
                        <ButtonModal
                            type="submit"
                            value="submit"
                            expanded={this.state.showWelcome}
                        ></ButtonModal>

                    
                        {this.props.errors[0]
                            ? <ErrorList errors={this.props.errors}></ErrorList>
                            : ""}
                     
                    </div>
                </form>
            </div>
        )
    }
}


const mapStateToProps = state => {
    let errors = [];
    if (state.auth.errors) {
        errors = Object.keys(state.auth.errors).map(field => {
            return {field, message:state.auth.errors[field]};
        });
    }
    return {
        errors,
        isAuthenticated: state.auth.isAuthenticated
    };
    
}

const mapDispatchToProps = dispatch => {
    return {
        register: (username, first_name, email, password) => {
            return dispatch(auth.register(username, first_name, email, password));
        }
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(Register);