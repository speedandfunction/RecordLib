import React, { useState } from "react";
import { connect } from "react-redux";
import Button from "@material-ui/core/Button";
import { EditPetitionFormConnected as EditPetitionForm } from "frontend/src/forms/EditPetition";

/**
 * NewPetitionForm
 *
 * A button. If you click that button, create a form for editing a new petition. Give the new petition an ID.
 */
export const NewPetitionForm = (props) => {
  const { nextPetitionId } = props;
  const [showNewForm, setShowNewForm] = useState(false);

  const handleButtonClick = () => {
    setShowNewForm(true);
  };

  return (
    <div>
      <Button onClick={handleButtonClick}>New Petition</Button>
      {showNewForm ? <EditPetitionForm petitionId={nextPetitionId} /> : <></>}
    </div>
  );
};

const mapStateToProps = (state) => {
  try {
    return {
      nextPetitionId:
        state.petitions.petitionCollection.entities.petitions.length,
    };
  } catch (err) {
    return {
      nextPetitionId: 0,
    };
  }
};

export const NewPetitionFormConnected = connect(mapStateToProps)(
  NewPetitionForm
);
