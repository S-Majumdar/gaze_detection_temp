import React from 'react'
import Header from './components/Header'
//import visual components
import { Button } from "@material-ui/core";
function HomePage() {

    return (
        <div className="App">
            <Header />
            <div className="homepage__buttons">
                <Button onClick={(event) => {
                    event.preventDefault();
                    console.log("Btn clicked");
                    window.location.href="/less_than_3_years";
                }} className="homepage__button" style={{ borderRadius: '90px', fontSize: '45px', minHeight: '300px' }} variant="contained">Less than 3 years of age</Button>

                <Button onClick={(event) => {
                     event.preventDefault();
                     console.log("Btn clicked");
                     window.location.href="/more_than_3_years";
                }} className="homepage__button" style={{ borderRadius: '90px', fontSize: '45px' }} variant="contained">More than 3 years of age</Button>
            </div>
        </div>
    )
}

export default HomePage
