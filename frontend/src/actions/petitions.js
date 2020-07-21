import { normalizePetitions } from "frontend/src/normalize/petitions";

export const NEW_PETITION = "NEW_PETITION";
export const UPDATE_PETITION = "UPDATE_PETITION";
export const NEW_CASE_FOR_PETITION = "NEW_CASE_FOR_PETITION";
export const SET_PETITION_TO_EDIT = "SET_PETITION_TO_EDIT";
export const DELETE_PETITION = "DELETE_PETITION";

/** An action to add a new petition to the application state */
export const newPetition = (petition) => {
  return {
    type: NEW_PETITION,
    payload: petition,
  };
};

/**Update the petition with `petitionId`, by merging the updateObject into it. */
export const updatePetition = (petitionId, updateObject) => {
  return {
    type: UPDATE_PETITION,
    payload: { petitionId, updateObject },
  };
};

/**Add a new case to a petition. */
export const newCaseForPetition = (petitionId, caseId, caseDefaults = {}) => {
  return {
    type: NEW_CASE_FOR_PETITION,
    payload: { petitionId, caseId, caseDefaults },
  };
};

/** Identify the petition that should be edited in the edit form. */
export const setPetitionToEdit = (petitionId) => {
  return {
    type: SET_PETITION_TO_EDIT,
    payload: { petitionId: petitionId },
  };
};

export const deletePetition = (petitionId) => {
  return {
    type: DELETE_PETITION,
    payload: { petitionId: petitionId },
  };
};
