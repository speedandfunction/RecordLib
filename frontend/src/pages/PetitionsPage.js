import React, { useState } from "react";
import { connect } from "react-redux";
import { makeStyles } from "@material-ui/core/styles";
import PropTypes from "prop-types";
import Button from "@material-ui/core/Button";
import Container from "@material-ui/core/Container";
import Paper from "@material-ui/core/Paper";
import { fetchPetitions } from "frontend/src/actions";
import Typography from "@material-ui/core/Typography";
import { NewPetitionFormConnected as NewPetitionForm } from "frontend/src/forms/NewPetition";
import { PetitionsTable } from "frontend/src/components/PetitionsTable";

const useStyles = makeStyles((theme) => {
  return {
    paper: {
      padding: theme.spacing(3),
      marginTop: theme.spacing(3),
    },
  };
});

function PetitionsPage(props) {
  const { petitions, attorney } = props;

  //defaultAttorney is a _copy_ of the attorney from state,
  // It must be a copy because its being sent as a default
  // to a NewPetition, and it can change independently
  // from the attorney in state.
  // ... note also the deep copy, since attorney has an address obj.
  const defaultAttorney = { ...attorney, address: { ...attorney.address } };

  const styles = useStyles();

  const [selectedPetitions, setSelectedPetitions] = useState(petitions);

  console.log("petitions");
  console.log(petitions);

  const [isReadyToSubmit, setIsReadyToSubmit] = useState(
    petitions && petitions.result && petitions.result.length > 0
  );

  const submitGetPetitions = (e) => {
    e.preventDefault();
    getPetitions(selectedPetitions, attorney);
  };

  const PetitionsPagetyle = {
    margin: "15px",
    border: "1px solid black",
    borderRadius: "25px",
    padding: "10px",
    width: "950px",
  };
  return (
    <Container>
      <Paper className={styles.paper}>
        <Typography variant="h3">Petitions</Typography>
        <form id="PetitionsPage" onSubmit={submitGetPetitions}>
          <Button type="submit" variant="contained" disabled={!isReadyToSubmit}>
            Process Petition Package
          </Button>
        </form>
        <div></div>
        <PetitionsTable />
        <NewPetitionForm />
      </Paper>
    </Container>
  );
}

PetitionsPage.propTypes = {
  petitions: PropTypes.object.isRequired,
};

function mapStateToProps(state) {
  return {
    petitions: state.petitions.petitionCollection,
    attorney: state.attorney,
  };
}

function mapDispatchToProps(dispatch, ownProps) {
  return {
    getPetitions: (selectedPetitions, atty) =>
      dispatch(fetchPetitions(selectedPetitions, atty)),
  };
}

const PetitionsPageWrapper = connect(
  mapStateToProps,
  mapDispatchToProps
)(PetitionsPage);
export default PetitionsPageWrapper;
