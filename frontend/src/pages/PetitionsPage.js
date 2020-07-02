import React, { useState } from "react";
import { connect } from "react-redux";
import { makeStyles } from "@material-ui/core/styles";
import PropTypes from "prop-types";
import Button from "@material-ui/core/Button";
import Container from "@material-ui/core/Container";
import Paper from "@material-ui/core/Paper";
import { fetchPetitions } from "frontend/src/actions";
import Typography from "@material-ui/core/Typography";
import Petition from "frontend/src/components/Petition";
import { NewPetitionForm } from "frontend/src/forms/NewPetition";
import ServiceAgencyList from "frontend/src/components/ServiceAgencyList";

const useStyles = makeStyles((theme) => {
  return {
    paper: {
      padding: theme.spacing(3),
      marginTop: theme.spacing(3),
    },
  };
});

function PetitionsPage(props) {
  const { petitions } = props;

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
          <ServiceAgencyList />
        </form>
        <div>
          <NewPetitionForm
            petitionId={
              petitions.result ? (petitions.result.length + 1).toString() : 0
            }
          />
        </div>
        <div>
          {petitions.length > 0 ? (
            petitions.map((petition, idx) => {
              return <Petition key={idx} petition={petition}></Petition>;
            })
          ) : (
            <p>
              There are no petitions to display yet. Have you conducted an
              analysis yet?
            </p>
          )}
        </div>
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
