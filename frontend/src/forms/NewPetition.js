import React, { useState } from "react";
import { connect } from "react-redux";
import Button from "@material-ui/core/Button";
import { EditPetitionFormConnected as EditPetitionForm } from "frontend/src/forms/EditPetition";
import { newPetition } from "frontend/src/actions/petitions";

/**
 * NewPetitionForm
 *
 * A button. If you click that button, create a form for editing a new petition. Give the new petition an ID.
 */
export const NewPetitionForm = (props) => {
  const { newPetitionId, editingPetitionId, newPetition } = props;
  const [showEditForm, setShowEditForm] = useState(false);

  const handleButtonClick = () => {
    newPetition(newPetitionId);
    setShowEditForm(true);
  };

  return (
    <div>
      <Button onClick={handleButtonClick}>New Petition</Button>
      {showEditForm ? (
        <EditPetitionForm petitionId={editingPetitionId} />
      ) : (
        <></>
      )}
    </div>
  );
};

const generatePetitionId = (petitionIds) => {
  return (Math.max(petitionIds.map((id) => parseInt(id))) + 1).toString();
};

const mapStateToProps = (state) => {
  return {
    newPetitionId: generatePetitionId(
      state.petitions.petitionCollection.petitionIds
    ),
    editingPetitionId: state.petitions.petitionCollection.editingPetitionId,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    newPetition: (newId) => {
      dispatch(newPetition({ id: newId }));
    },
  };
};

export const NewPetitionFormConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(NewPetitionForm);
