import React from "react"
import Button from "@material-ui/core/Button"
import PropTypes from 'prop-types'
import { makeStyles } from "@material-ui/core/styles" 


const useStyles = makeStyles(theme => ({
    item: {
        margin: "0.5rem",
    }
}))





function GradeTableItem(props) {
    const { grade, prob, modifier} = props
    const classes = useStyles()

    const createClickHandler = (grade, chargeId) => {
        return (
            (e) => modifier(grade)
        )
    }

    return (<Button 
                className={classes.item} 
                item 
                onClick={createClickHandler(grade)}
                {...props}> {grade}: {prob*100}%</Button>)
}




GradeTableItem.propTypes = {
    grade: PropTypes.string.isRequired,
    prob: PropTypes.number.isRequired,
}


export default GradeTableItem;