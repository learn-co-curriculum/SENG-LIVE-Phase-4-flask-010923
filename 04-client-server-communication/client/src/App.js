// 📚 Review With Students:
    // Request response cycle
    //Note: This was build using v5 of react-router-dom
import { Route, Switch, useHistory } from 'react-router-dom'
import {createGlobalStyle} from 'styled-components'
import {useEffect, useState} from 'react'
import Home from './components/Home'
import ProductionForm from './components/ProductionForm'
import ProductionEdit from './components/ProductionEdit'
import Navigation from './components/Navigation'
import ProductionDetail from './components/ProductionDetail'
import NotFound from './components/NotFound'

const baseUrl = 'http://127.0.0.1:5555'
const productionsUrl = baseUrl + '/productions'

function App() {
  const [productions, setProductions] = useState([])
  const [production_edit, setProductionEdit] = useState(false)

  const [ errors, setErrors ] = useState( null )

  const history = useHistory()
  // 4.✅ GET Productions from our Flask API
  useEffect( () => fetchProductions(), [] )

  const fetchProductions = () =>
    fetch( productionsUrl )
    .then( r => r.json() )
    .then( setProductions )
  
  // 5.✅ navigate to client/src/components/ProductionForm.js and get the form working
  const createNewProduction = ( new_prod, event ) => {
    event.preventDefault()

    const postRequest = {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'accept': 'application/json'
      },
      body: JSON.stringify( new_prod )
    }

    fetch( productionsUrl, postRequest )
    .then( r => r.json() )
    .then( new_prod_data => {
      if ( new_prod_data.errors ) {
        setErrors( new_prod_data.errors )
      }
      else {
        setErrors( null )
        setProductions( [ ...productions, new_prod_data ] )
      }
    })

  }

  // 6.✅ Get the ProductionDetail component up and running 

  // 7.✅ Navigate to the ProductionEdit.js and hook it up

  const addProduction = (production) => setProductions(productions => [...productions,production])
  const updateProductions = (updated_production) => setProductions(productions => productions.map(production =>{
    if(production.id === updated_production.id){
      return updated_production
    } else {
      return production
    }
  } ))
  const deleteProduction = (deleted_production) => setProductions(productions => productions.filter((production) => production.id !== deleted_production.id) )

  const handleEdit = (production) => {
    setProductionEdit(production)
    history.push(`/productions/edit/${production.id}`)
  }

  return (
    <>
    <GlobalStyle />
    <Navigation handleEdit={handleEdit}/>
      <Switch>
        <Route  path='/productions/new'>
          <ProductionForm
            addProduction={addProduction}
            createNewProduction = { createNewProduction }
            errors = { errors }
          />
        </Route>
        <Route  path='/productions/edit/:id'>
          <ProductionEdit 
            updateProductions={updateProductions} 
            production_edit={production_edit}
            productionsUrl={productionsUrl}
          />
        </Route>
        <Route path='/productions/:id'>
            <ProductionDetail 
              handleEdit={handleEdit} 
              deleteProduction={deleteProduction} 
              productionsUrl = { productionsUrl }
            />
        </Route>
        <Route exact path='/'>
          <Home  productions={productions} />
        </Route>
        <Route>
          <NotFound />
        </Route>
      </Switch>
    </>
  )
}

export default App

const GlobalStyle = createGlobalStyle`
    body{
      background-color: black; 
      color:white;
    }
    `

