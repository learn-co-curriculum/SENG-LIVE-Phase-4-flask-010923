import { useState } from 'react'
import {Link} from 'react-router-dom'
import styled from 'styled-components'
import { useHistory } from 'react-router-dom'
import { GiHamburgerMenu } from 'react-icons/gi'

function Navigation({updateUser}) {
 const [menu, setMenu] = useState(false)
 const history = useHistory()

 // 6.✅ Build a DELETE fetch request
  //6.1 On a successful delete clear the user from state (updateUser is passed down from app via props) and redirect back to the authentication route
// 7.✅ Head back to server/app.py to build a route that will keep our user logged in with sessions
 const handleLogout = () => {
  
 }

    return (
        <Nav> 
         <NavH1>Flatiron Theater Company</NavH1>
         <Menu>
           {!menu?
           <div onClick={() => setMenu(!menu)}>
             <GiHamburgerMenu size={30}/> 
           </div>:
           <ul>
            <li onClick={() => setMenu(!menu)}>x</li>
            <li><Link to='/productions/new'>New Production</Link></li>
            <li><Link to='/'> Home</Link></li>
            <li><Link to='/authentication'> Login/Signup</Link></li>
            <li onClick={handleLogout}> Logout </li>
           </ul>
           }
         </Menu>

        </Nav>
    )
}

export default Navigation


const NavH1 = styled.h1`
font-family: 'Splash', cursive;
`
const Nav = styled.div`
  display: flex;
  justify-content:space-between;
  
`;

const Menu = styled.div`
  display: flex;
  align-items: center;
  a{
    text-decoration: none;
    color:white;
    font-family:Arial;
  }
  a:hover{
    color:pink
  }
  ul{
    list-style:none;
  }
  
`;
