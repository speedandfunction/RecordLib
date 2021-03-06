import React from "react";
import Container from "@material-ui/core/Container"
import Paper from "@material-ui/core/Paper"
import { makeStyles } from "@material-ui/core/styles"

const useStyles = makeStyles(theme =>  {
    return({
        paper: {
            padding: theme.spacing(3),
            marginTop: theme.spacing(3),
        }
    })
})

import ApplicantHolderWrapper from "./ApplicantHolder";
import NameSearch from "./NameSearch"
function GettingStarted(props) {
    const classes = useStyles()
    return (
        <Container>
            <Paper className={classes.paper}>
                <div className="gettingStarted" >
                    <div style={{color: 'red'}}>Please enter the applicant's address, social security  number, and any
                    other information which will not be provided by uploaded files.</div>
                    <ApplicantHolderWrapper />
                </div>
                <NameSearch />
            </Paper>
        </Container>
    );
};

export default GettingStarted;