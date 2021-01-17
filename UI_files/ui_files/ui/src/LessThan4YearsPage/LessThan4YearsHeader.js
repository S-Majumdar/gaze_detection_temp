import React from 'react'
import '../components/Header.css'
//importing react/material-ui ui components
import HomeIcon from '@material-ui/icons/Home';
import IconButton from '@material-ui/core/IconButton';
import HelpOutlineIcon from '@material-ui/icons/HelpOutline';

function LessThan4YearsHeader() {
    return (
        <div className="header">
            <IconButton>
                <HomeIcon onClick={(event) => {
                    event.preventDefault();
                    window.location.href="/";
                }} fontSize="large" className="header__icon" />
            </IconButton>
            <div className="homepage__welcome_message" >Please watch the video and save the recording once video ends</div>
            <IconButton>
                <HelpOutlineIcon fontSize="large" className="header__icon" />    
            </IconButton>            
        </div>
    )
}

export default LessThan4YearsHeader
