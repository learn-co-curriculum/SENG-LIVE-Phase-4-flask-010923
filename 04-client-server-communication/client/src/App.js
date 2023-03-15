// 📚 Review With Students:
    // Request response cycle
    //Note: This was build using v5 of react-router-dom
import { Route, Switch } from 'react-router-dom'
import {createGlobalStyle} from 'styled-components'
import {useEffect, useState} from 'react'
import Home from './components/Home'
import ProductionForm from './components/ProductionForm'
import Navigation from './components/Navigation'
import ProductionDetail from './components/ProductionDetail'
import NotFound from './components/NotFound'

function App() {
  const [productions, setProductions] = useState([])
  //5.✅ GET Productions
  // 5.1 Invoke the useEffect() hook
  // 5.2 Build a fetch request to '/productions'
    // Note: The proxy in package.json has been set to "http://localhost:5000"
    // This will allow us to proxy our api requests  
  // 5.3 When productions return set the productions to state
  // 6.✅ navigate to client/src/components/ProductionForm.js

  // Bonus: async and await version
  // useEffect(async () => {
  //   const res = await fetch('/productions')
  //   const productions = await res.json()
  //   setProductions(productions)
  // },[])

  const addProduction = (production) => setProductions(current => [...current,production])

  return (
    <>
    <GlobalStyle />
    <Navigation/>
      <Switch>
        <Route  path='/productions/new'>
          <ProductionForm addProduction={addProduction}/>
        </Route>
        <Route path='/productions/:id'>
            <ProductionDetail />
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

