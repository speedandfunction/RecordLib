import React from "react"
import Button from "@material-ui/core/Button"

import { connect } from "react-redux"
import { guessGrade } from "../actions/grades"

/**
 * Extract the components of a statute's string into an object with props title, section, subsection.
 * @param {} statute 
 */
function getStatuteComponents(statute) {
    const parts = statute.split(' ')

    const components = {
        title: parts[0],
        section: parts[1],
        subsection: parts.slice(2).join('')
    }

    return components
}

/** Button for trigging an action to predict the grade of an offense. 
 * 
*/
function PredictGradeButton(props) {

    const {id, offense, statute, guessGrade } = props

    const isAvailable = offense && statute

    const components = getStatuteComponents(statute)

    const clickHandler = (id, offense, components) => {
        return (e) => {
            guessGrade(id, offense, components)
        }
    }

    return(
        <Button 
            disabled={!isAvailable}
            onClick={clickHandler(id, offense, components)}> 
            Predict Grade 
        </Button>
    ) 
}

function mapDispatchToProps(dispatch) {
    return {
        guessGrade: (id, offense, statuteComponents) => {
            dispatch(guessGrade(id, offense, statuteComponents))
        }
    }
}

const PredictGradeButtonWrapper = connect(null, mapDispatchToProps)(PredictGradeButton)

export default PredictGradeButtonWrapper