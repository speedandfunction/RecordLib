import { normalizePetitions } from "frontend/src/normalize/petitions";

export const NEW_PETITION = "NEW_PETITION";
export const UPDATE_PETITION = "UPDATE_PETITION";

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
