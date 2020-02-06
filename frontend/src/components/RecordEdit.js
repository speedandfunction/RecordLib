import React, { useState } from "react"
import { connect } from "react-redux"
import { Redirect } from "react-router-dom"
import CRecordWrapper from "./CRecord"
import Container from "@material-ui/core/Container"
import FormGroup from "@material-ui/core/FormGroup"
import Button from "@material-ui/core/Button"
import { analyzeCRecord } from "../actions/crecord"


function RecordEdit(props) {
    const { crecordFetched, analyzeCRecord } = props 
  
    const [redirectTo, setRedirectTo] = useState(null)

    function clickHandler(redirectDest) {
        return((e) => { 
            e.preventDefault()
            setRedirectTo(redirectDest)  
            analyzeCRecord()
        })
    }

    if (redirectTo !== null) {
        return(
            <Redirect to={redirectTo}/>
        )
    }

    return (
        <Container>
            <Button type="submit" onClick={clickHandler("/analysis")}> Analyze </Button>
            {crecordFetched? <CRecordWrapper/> : <p> No Record yet (process for making a new record will go here) </p>}
        </Container>
    )
}

function mapStateToProps(state) {
    return {crecordFetched: state.crecord? true: false}
}

function mapDispatchToProps(dispatch) {
    return {analyzeCRecord: () => {
        dispatch(analyzeCRecord()) 
    }}
}

export default connect(mapStateToProps, mapDispatchToProps)(RecordEdit)
