import React, {useState} from 'react'
import styled from 'styled-components'
import { useHistory } from 'react-router-dom'
// 6.✅ Verify formik and yet have been added to our package.json dependencies 
  // import the useFormik hook from formik
  // import * as yup for yup



function ProductionForm({addProduction}) {

  const history = useHistory()
  // 7.✅ Use yup to create client side validations
 


  // 9.✅ useFormik hook


    return (
      <div className='App'>
      <Form >
        <label>Title </label>
        <input type='text' name='title' />
        
        <label> Genre</label>
        <input type='text' name='genre' />
      
        <label>Budget</label>
        <input type='number' name='budget' />
      
        <label>Image</label>
        <input type='text' name='image'  />
      
        <label>Director</label>
        <input type='text' name='director'/>
      
        <label>Description</label>
        <textarea type='text' rows='4' cols='50' name='description' />
      
        <input type='submit' />
      </Form> 
      </div>
    )
  }
  
  export default ProductionForm

  const Form = styled.form`
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