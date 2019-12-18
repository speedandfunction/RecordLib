import { GUESS_GRADE_SUCCEEDED } from "../actions/grades"

/**
 * Reducers for a slice of state relating to gussing grades.
 */


function gradeProbabilitiesReducer(state = {}, action) {
    switch(action.type) {
        case GUESS_GRADE_SUCCEEDED:
            const { chargeId, gradeProbabilities } = action.payload
            return Object.assign({}, state, {[chargeId]: gradeProbabilities})
        default: 
            return(state)
    }
}

export default gradeProbabilitiesReducer
