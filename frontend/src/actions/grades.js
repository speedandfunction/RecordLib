/**
 * Actions for interacting with the /grades/ api endpoints. This is for predicting grades of offenses
 * with missing grades.
 */

import * as api from "../api"

export const GUESS_GRADE_SUCCEEDED = "GUESS_GRADE_SUCCEEDED"


function guessGradeSucceeded(chargeId, gradeProbabilities) {
    return({
        type: GUESS_GRADE_SUCCEEDED,
        payload: {chargeId, gradeProbabilities}
    })
}

export function guessGrade(chargeId, offense, statute) {
    return dispatch => {
        api.guessGrade(offense, statute)
           .then((resp) => {
               dispatch(guessGradeSucceeded(chargeId, resp.data))
           })
           .catch(err => {
               console.log("guess grade api call failed.")
               console.log(err)
           })
    }
}