import React, { useState } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import TextField from "@material-ui/core/TextField";
import IconButton from "@material-ui/core/IconButton";
import AddIcon from "@material-ui/icons/Add";
import { addAlias } from "frontend/src/actions/applicant.js";

function AddAlias(props) {
  const { adder } = props;
  const [name, setName] = useState("");

  const handleChange = (event) => setName(event.target.value);
  const handleClick = () => {
    adder(name);
    setName("");
  };

  const handleKeyDown = (event) => {
    if (event.keyCode === 13) {
      event.preventDefault();
      event.stopPropagation();
      handleClick();
    }
  };

  return (
    <div className="addAlias">
      <TextField
        label="Alias"
        type="text"
        value={name}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
      />
      <IconButton
        size="small"
        type="button"
        style={{ marginLeft: "20px" }}
        onClick={handleClick}
        aria-label="add"
      >
        <AddIcon />
      </IconButton>
    </div>
  );
}

function mapDispatchToProps(dispatch) {
  return {
    adder: (name) => {
      dispatch(addAlias(name));
    },
  };
}

AddAlias.propTypes = {
  /**
   * The callback which adds the alias to state.
   */
  adder: PropTypes.func.isRequired,
};

const AddAliasWrapper = connect(null, mapDispatchToProps)(AddAlias);
export default AddAliasWrapper;
