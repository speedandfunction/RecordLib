import React from "react";
import Container from "@material-ui/core/Container";
import Paper from "@material-ui/core/Paper";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import ServiceAgencyList from "frontend/src/components/ServiceAgencyList";
import AttorneyHolderWrapper from "frontend/src/components/AttorneyHolder";

const useStyles = makeStyles((theme) => {
  return {
    paper: {
      padding: theme.spacing(3),
      marginTop: theme.spacing(3),
    },
  };
});

/**Attorney page - page for editing the attorney signing a set of Petitions.
 *
 */
function AttorneyPage(props) {
  const classes = useStyles();
  return (
    <Container>
      <Paper className={classes.paper}>
        <div className="gettingStarted">
          <Typography variant="h3">Attorney</Typography>
          <Typography variant="body1">
            Please enter details of the attorney signing onto this set of
            petitions.
          </Typography>

          <AttorneyHolderWrapper />
        </div>
        <div>
          <h3> Other defaults</h3>

          <ServiceAgencyList />
        </div>
      </Paper>
    </Container>
  );
}

export default AttorneyPage;
