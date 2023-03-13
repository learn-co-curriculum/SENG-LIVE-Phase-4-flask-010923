import React, {useState} from 'react'
import styled from 'styled-components'
import { useHistory } from 'react-router-dom'
// 6.✅ Verify formik and yet have been added to our package.json dependencies 
  // import the useFormik hook from formik
  // import * as yup for yup


function ProductionForm({addProduction}) {
  const history = useHistory()
  // 7.✅ Use yup to create client side validations
    // 7.1 validations
    // Every form field is required 
    // title, genre, and description should have character limits.
    // Budget should be a positive number
    // Note: ongoing is set to True by default on our server.
    


  // 9.✅ useFormik hook
    // 9.1 the useFormik hook takes an object.
    // 9.2 Create a key called initialValues and set it to an object.
        //9.2.a The object should contain every form field
        // Note: Ongoing is missing because ongoing is set to True by default on our server.
    // 9.3 Create a key called validationSchema assigned with formSchema and onSubmit
        // 9.3.1 onSubmit is assigned an arrow function which calls our POST request to '/productions'. Pass the arrow function a param called 'values'
        // 9.3.2 In the body of the post stringify, values, null and 2
        // 9.3.3 When the POST returns add the new production to state and redirect to the page of the new Production
 
   // 9.✅ use formik to handle the Submit and Change events
    return (
      <div className='App'>

      <Form >
        <label>Title </label>
        <input type='text' name='title'  />
        
        <label> Genre</label>
        <input type='text' name='genre'  />
      
        <label>Budget</label>
        <input type='number' name='budget'  />
      
        <label>Image</label>
        <input type='text' name='image'  />
      
        <label>Director</label>
        <input type='text' name='director'  />
      
        <label>Description</label>
        <textarea type='text' rows='4' cols='50' name='description'  />
      
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