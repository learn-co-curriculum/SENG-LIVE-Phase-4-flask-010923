import React, {useState} from 'react'
import styled from 'styled-components'
import { useHistory } from 'react-router-dom'
import { useFormik } from "formik"
import * as yup from "yup"


function ProductionForm({updateProduction, production_edit}) {
  const history = useHistory()
    const formSchema = yup.object().shape({
      title: yup.string().required("Must enter a title"),
      budget: yup.number().positive()
    })
        const formik = useFormik({
          initialValues: {
            title: production_edit.title,
            genre: production_edit.genre,
            budget: production_edit.budget,
            image: production_edit.image,
            director:  production_edit.director,
            description: production_edit.description,
          },
          validationSchema: formSchema,
          onSubmit: (values) => {
            fetch(`/productions/${production_edit.id}`,{
              method:'PATCH',
              headers:{
                "Content-Type":"application/json"
              },
              body: JSON.stringify(values, null, 2)
            })
            .then(res => res.json())
            .then(production => {
              updateProduction(production)
              history.push(`/productions/${production.id}`)
            })
          },
        })

    return (
      <div className='App'>
      {formik.errors&& Object.values(formik.errors).map(error => <h2>{error}</h2>)}
      <Form onSubmit={formik.handleSubmit}>
        <label>Title </label>
        <input type='text' name='title' value={formik.values.title} onChange={formik.handleChange}  />
        
        <label> Genre</label>
        <input type='text' name='genre' value={formik.values.genre} onChange={formik.handleChange}  />
      
        <label>Budget</label>
        <input type='number' name='budget' value={formik.values.budget} onChange={formik.handleChange} />
      
        <label>Image</label>
        <input type='text' name='image' value={formik.values.image} onChange={formik.handleChange}  />
      
        <label>Director</label>
        <input type='text' name='director' value={formik.values.director} onChange={formik.handleChange}  />
      
        <label>Description</label>
        <textarea type='text' rows='4' cols='50' name='description'  value={formik.values.description} onChange={formik.handleChange} />
      
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