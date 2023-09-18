import  {useParams, useHistory } from 'react-router-dom'
import {useEffect, useState} from 'react'
import styled from 'styled-components'

function ProductionDetail({handleEdit, deleteProduction, productionsUrl}) {
  const [ production, setProduction ] = useState({cast:[]})
  const [ errors, setErrors ] = useState(null)
  //Student Challenge: GET One 
  const params = useParams()
  const history = useHistory()
  useEffect(()=>{
    fetch( productionsUrl + `/${params.id}` )
    .then( r => r.json() )
    .then( setProduction )

  },[])

  console.log( params.id )

  const handleDelete = (production) => {

  }

  
  const {id, title, genre, image,description, cast} = production 
  if( errors )
    return (
      <div>
        { errors.map( error => <h2>{ error }</h2> ) }
      </div>
    )
  return (
      <CardDetail id={id}>
        <h1>{title}</h1>
          <div className='wrapper'>
            <div>
              <h3>Genre:</h3>
              <p>{genre}</p>
              <h3>Description:</h3>
              <p>{description}</p>
              <h2>Cast Members</h2>
              <ul>
                {cast.map(cm => <li>{`${cm.role} : ${cm.name}`}</li>)}
              </ul>
            </div>
            <img src={image}/>
          </div>
      <button onClick={()=> handleEdit(production)} >Edit Production</button>
      <button onClick={()=> handleDelete(production)} >Delete Production</button>
      </CardDetail>
    )
  }
  
  export default ProductionDetail
  const CardDetail = styled.li`
    display:flex;
    flex-direction:column;
    justify-content:start;
    font-family:Arial, sans-serif;
    margin:5px;
    h1{
      font-size:60px;
      border-bottom:solid;
      border-color:#42ddf5;
    }
    .wrapper{
      display:flex;
      div{
        margin:10px;
      }
    }
    img{
      width: 300px;
    }
    button{
      background-color:#42ddf5;
      color: white;
      height:40px;
      font-family:Arial;
      font-size:30px;
      margin-top:10px;
    }
  `