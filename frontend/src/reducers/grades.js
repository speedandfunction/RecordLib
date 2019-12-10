import { combineReducers } from 'redux';
import { GUESS_GRADE_SUCCEEDED } from "../actions/grades"
/**
 * Reducers for a slice of state relating to gussing grades.
 */


function gradePredictionReducer(state = {}, action) {
    switch(action.type) {
        case GUESS_GRADE_SUCCEEDED:
            const { chargeId, gradeProbabilities } = action.payload
            return Object.assign({}, state, {[chargeId]: gradeProbabilities})
        default: 
            return(state)
    }
}

export default gradePredictionReducer
