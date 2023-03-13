import React, {useState} from 'react'
import {useHistory} from 'react-router-dom'
import styled from "styled-components";
import { useFormik } from "formik"
import * as yup from "yup"


function Authentication({updateUser}) {
  const [signUp, setSignUp] = useState(false)
  const history = useHistory()

  const handleClick = () => setSignUp((signUp) => !signUp)
  // 3.✅ Finish building the authentication form with formik
    // 3.1 create a formSchema and use yup to make some client side validations
    // 3.2 Use formik to handle the value, onchange and onsubmit of the form
    // 3.3 on submit create a POST. 
      // 3.4 There is a button that toggles the component between login and sign up.
      // if signUp is true use the path '/users' else use '/login' (we will be writing login soon)
      // Complete the post and test our '/users' route 
    // 3.4 On a successful POST add the user to state (updateUser is passed down from app through props) and redirect to the Home page.
  // 4.✅ return to server/app.py to build the next route
 
    return (
        <> 
        <h2 style={{color:'red'}}> {'Errors Here!!'}</h2>
        <h2>Please Log in or Sign up!</h2>
        <h2>{signUp?'Already a member?':'Not a member?'}</h2>
        <button onClick={handleClick}>{signUp?'Log In!':'Register now!'}</button>
        <Form onSubmit={console.log}>
        <label>
          Username
          </label>
        <input type='text' name='name' value={'value'} onChange={console.log} />
        {signUp&&(
          <>
          <label>
          Email
          </label>
          <input type='text' name='email' value={'value'} onChange={console.log} />
          </>
        )}
        <input type='submit' value={signUp?'Sign Up!':'Log In!'} />
      </Form>
        </>
    )
}

export default Authentication

export const Form = styled.form`
display:flex;
flex-direction:column;
width: 400px;
margin:auto;
font-family:Arial;
font-size:30px;
input[type=submit]{
  background-color:#42ddf5;
  color: white;
  height:40px;
  font-family:Arial;
  font-size:30px;
  margin-top:10px;
  margin-bottom:10px;
}
`