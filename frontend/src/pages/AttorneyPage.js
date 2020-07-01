import React from "react";
import Container from "@material-ui/core/Container";
import Paper from "@material-ui/core/Paper";
import { makeStyles } from "@material-ui/core/styles";

import AttorneyHolderWrapper from "frontend/src/components/AttorneyHolder";
import NameSearch from "frontend/src/components/NameSearch";

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
          <div style={{ color: "red" }}>
            Please enter details of the attorney signing onto this set of
            petitions.
          </div>
          <AttorneyHolderWrapper />
        </div>
        <NameSearch />
      </Paper>
    </Container>
  );
}

export default AttorneyPage;
