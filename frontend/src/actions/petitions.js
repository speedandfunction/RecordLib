import {
  normalizePetitions,
  denormalizePetitions,
} from "frontend/src/normalize/petitions";
import * as api from "../api";

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
export const newCaseForPetition = (
  petitionId,
  caseId,
  caseDefaults = {},
  chargeInfo = {}
) => {
  return {
    type: NEW_CASE_FOR_PETITION,
    payload: { petitionId, caseId, caseDefaults, chargeInfo },
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

function fetchPetitionsSucceeded(petitionPath) {
  return {
    type: "FETCH_PETITIONS_SUCCEEDED",
  };
}

/**
 * Create an action that sends a list of petitions to the server, and returns the files.
 * @param {} petitions
 */
export function fetchPetitions(petitionIds, petitions, cases, charges) {
  const denormalized = denormalizePetitions(petitionIds, {
    petitions,
    cases,
    charges,
  });
  console.log("fetching petitions");
  console.log(petitions);
  console.log(cases);
  console.log(charges);

  console.log("denormalized petitions:");
  console.log(denormalized);

  return (dispatch, getState) => {
    api
      .fetchPetitions(denormalized)
      .then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "ExpungementPetitions.zip");
        document.body.appendChild(link);
        link.click();
        console.log("fetched petitions successfully");
        dispatch(fetchPetitionsSucceeded());
      })
      .catch((err) => console.log("error fetching petitions."));
  };
}
