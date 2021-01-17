import React from 'react'
import './Header.css'
//importing react/material-ui ui components
import HomeIcon from '@material-ui/icons/Home';
import IconButton from '@material-ui/core/IconButton';
import HelpOutlineIcon from '@material-ui/icons/HelpOutline';

function Header() {
    return (
        <div className="header">
            <IconButton>
                <HomeIcon onClick={(event) => {
                    event.preventDefault();
                    window.location.href="/";
                }} fontSize="large" className="header__icon" />
            </IconButton>
            <div className="homepage__welcome_message" >Welcome to the Autism Detection App. Please select your age group.</div>
            <IconButton>
                <HelpOutlineIcon fontSize="large" className="header__icon" />    
            </IconButton>            
        </div>
    )
}

export default Header
