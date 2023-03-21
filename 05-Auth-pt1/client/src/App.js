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
import Authentication from './components/Authentication'

function App() {
  const [productions, setProductions] = useState([])
  const [productionEdit, setProductionEdit] = useState([])
  const [user, setUser] = useState(null)
  const history = useHistory()

  useEffect(() => {
   
    fetchProductions()
  },[])

  const fetchProductions = () => (
    fetch('/productions')
    .then(res => res.json())
    .then(setProductions)
  )

  const fetchUser = () => {
    // 8.✅ Create a GET fetch that goes to '/authorized'
      // If returned successfully set the user to state and fetch our productions
      // else set the user in state to Null
   
}
 
  const addProduction = (production) => setProductions(current => [...current,production])
  const updateProduction = (updated_production) => setProductions(productions => productions.map(production => production.id == updated_production.id? updated_production : production))
  const deleteProduction = (deleted_production) => setProductions(productions => productions.filter((production) => production.id !== deleted_production.id) )
  const handleEdit = (production) => {
    setProductionEdit(production)
    history.push(`/productions/edit/${production.id}`)
  }
  
  const updateUser = (user) => setUser(user)
  // 9.✅ Return a second block of JSX
    // If the user is not in state return JSX and include <GlobalStyle /> <Navigation/> and  <Authentication updateUser={updateUser}/>
    //9.1 Test out our route! Logout and try to visit other pages. Login and try to visit other pages again. Refresh the page and note that you are still logged in! 
  
  return (
    <>
    <GlobalStyle />
    <Navigation updateUser={updateUser}  handleEdit={handleEdit}/>
      <Switch>
        <Route path='/productions/new'>
          <ProductionForm addProduction={addProduction}/>
        </Route>
        <Route  path='/productions/edit/:id'>
          <ProductionEdit updateProduction={updateProduction} productionEdit={productionEdit}/>
        </Route>
        <Route path='/productions/:id'>
          <ProductionDetail handleEdit={handleEdit} deleteProduction={deleteProduction} />
        </Route>
        <Route exact path='/authentication'>
          <Authentication updateUser={updateUser}/>
        </Route>
        <Route exact path='/'>
          <Home  productions={productions}/>
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

