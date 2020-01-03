import React from "react"
import Tooltip from "@material-ui/core/Tooltip"
import Button from "@material-ui/core/Button"
import { makeStyles } from "@material-ui/core/styles"
import { connect } from "react-redux"
import { guessGrade } from "../actions/grades"


const useStyles = makeStyles(theme => ({
    button: {
        borderRadius: "100%",
        minWidth: 0,
    },

}))

/**
 * Extract the components of a statute's string into an object with props title, section, subsection.
 * @param {} statute 
 */
function getStatuteComponents(statute) {
    const parts = statute.replace(/§/g, ' ').split(' ').filter(w => w !== "")
    console.log("statute")
    console.log(statute)
    console.log("components")
    console.log(parts)
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
    const classes = useStyles()

    const {id, offense, statute, guessGrade } = props

    const isAvailable = offense && statute

    const components = getStatuteComponents(statute)

    const clickHandler = (id, offense, components) => {
        return (e) => {
            guessGrade(id, offense, components)
        }
    }

    return(
        <Tooltip title="Predict Grades">
            <span>
                <Button 
                    size="small"
                    className={classes.button}
                    variant="outlined"    
                    disabled={!isAvailable}
                    onClick={clickHandler(id, offense, components)}> 
                    P 
                </Button>
            </span>
        </Tooltip>
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