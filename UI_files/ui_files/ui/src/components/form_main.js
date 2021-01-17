import React from 'react'
import './form_main_css.css'

function Form_Main() {
    return (
        <div className="form_main">
            <div className="login-box">
                <h2>Autism Disorder Survey</h2>
                <form>
                    <div className="user-box">
                        <input type="text" name="" required="" />
                        <label>Name</label>
                    </div>
                    <div className="user-box">
                        <input type="number" name="" required="" />
                        <label>Age (In Years)</label>
                    </div>
                    <div className="user-box">
                        <input type="text" name="" required="" />
                        <label>Gender</label>
                    </div>
                    <div className="user-box">
                        <input type="email" name="" required="" />
                        <label>Email</label>
                    </div>
                    <div className="user-box1">
                        <textarea className="input" name="" required=""></textarea>
                        <label>Previous Diagnosis For Any ASD? (if any)</label>
                    </div>
                    <div className="user-box1">
                        <textarea className="input" name="" required=""></textarea>
                        <label>Symptoms Seen (If Any)</label>
                    </div>
                    <div className="input_field">
                        <label>
                            ASD Disorder(s) Suspected:
					<br />
                            <input type="checkbox" id="Asperger's syndrome" name="Asperger's syndrome" value="Asperger's syndrome" />
                            <label for="Asperger's syndrome">Asperger's syndrome</label>
                            <br />
                            <input type="checkbox" id="Autistic disorder" name="Autistic disorder" value="Autistic disorder" />
                            <label for="Autistic disorder">Autistic disorder</label>
                            <br />
                            <input type="checkbox" id="Childhood disintegrative disorder" name="Childhood disintegrative disorder" value="Childhood disintegrative disorder" />
                            <label for="Childhood disintegrative disorder">Childhood disintegrative disorder</label>
                            <br />
                            <input type="checkbox" id="Pervasive developmental disorder" name="Pervasive developmental disorder" value="Pervasive developmental disorder" />
                            <label for="Pervasive developmental disorder">Pervasive developmental disorder</label>
                        </label>
                    </div>
                    <a style={{ cursor: "pointer" }} onClick={(event) => {
                        event.preventDefault();
                        window.location.href = "/homepage"
                    }}>
                        <span></span>
                        <span></span>
                        <span></span>
                        <span></span>
                Submit
                </a>
                </form>
            </div>
        </div>
    )
}

export default Form_Main
