import React from "react";
/**
 * Form for adding a new petition
 */

export const NewPetitionForm = (props) => {
  const { petitionId } = props;

  return (
    <form id="newPetition">
      <div>Petition {petitionId}</div>
    </form>
  );
};
