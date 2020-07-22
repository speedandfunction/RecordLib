import React from "react";
import { connect } from "react-redux";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import Button from "@material-ui/core/Button";
import {
  setPetitionToEdit,
  deletePetition,
} from "frontend/src/actions/petitions";

const useStyles = makeStyles((theme) => {
  return {
    card: {
      minWidth: "128px",
      padding: ".5em",
      paddingBottom: "1em",
      marginBottom: "2em",
    },
    header: {
      fontSize: 18,
    },
  };
});

/**
 * Display information about a petition that could be generated.
 */
export function Petition(props) {
  const { petition, setPetitionToEdit, deletePetition } = props;
  const classes = useStyles();
  const handleEditPetition = (e) => {
    setPetitionToEdit(petition.id);
  };

  const handleDeletePetition = (e) => {
    deletePetition(petition.id);
  };

  return (
    <Card className={classes.card}>
      <CardContent>
        <Typography className={classes.header} color="textSecondary">
          {petition.petition_type}
        </Typography>
      </CardContent>
      <CardContent>
        <Typography variant="body2" color="textSecondary" component="p">
          {petition.id}
        </Typography>
        <Typography variant="body2" color="textSecondary" component="p">
          {petition.expungement_type ? petition.expungement_type : ""}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Attorney:{" "}
          {petition.attorney
            ? petition.attorney.full_name + " " + petition.attorney.organization
            : ""}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Client:{" "}
          {petition.client
            ? `${petition.client.first_name} ${petition.client.last_name}`
            : ""}
        </Typography>
        <Typography varian="body2" color="textSecondary">
          {petition.ifp_message}
        </Typography>
        <Typography variant="body2" color="textSecondary" component="p">
          {petition.cases ? `${petition.cases.length} cases.` : ""}
        </Typography>
        <List>
          {petition.cases ? (
            petition.cases.map((caseObject, idx) => {
              return (
                <ListItem key={idx}>
                  {" "}
                  <ListItemText primary={caseObject.docket_number}>
                    {" "}
                  </ListItemText>
                </ListItem>
              );
            })
          ) : (
            <></>
          )}
        </List>
        <Button onClick={handleEditPetition}>Edit</Button>
        <Button onClick={handleDeletePetition}>Delete</Button>
      </CardContent>
    </Card>
  );
}

const mapStateToProps = (state, ownProps) => {
  const { petitionId } = ownProps;
  const petition =
    state.petitions.petitionCollection.entities.petitions[petitionId];

  return {
    petition: petition,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    setPetitionToEdit: (petitionId) => dispatch(setPetitionToEdit(petitionId)),
    deletePetition: (petitionId) => dispatch(deletePetition(petitionId)),
  };
};

export const PetitionConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(Petition);
