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

function App() {
  const [productions, setProductions] = useState([])
  const [production_edit, setProductionEdit] = useState(false)
  const history = useHistory()
  //5.✅ GET Productions
  useEffect(()=>{
    fetch('/productions')
    .then(res => res.json())
    .then(setProductions)
  },[])

  
  // 6.✅ navigate to client/src/components/ProductionForm.js

  const addProduction = (production) => setProductions(productions => [...productions,production])
  const updateProduction = (updated_production) => setProductions(productions => productions.map(production =>{
    if(production.id == updated_production.id){
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
          <ProductionForm addProduction={addProduction}/>
        </Route>
        <Route  path='/productions/edit/:id'>
          <ProductionEdit updateProduction={updateProduction} production_edit={production_edit}/>
        </Route>
        <Route path='/productions/:id'>
            <ProductionDetail handleEdit={handleEdit} deleteProduction={deleteProduction} />
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

