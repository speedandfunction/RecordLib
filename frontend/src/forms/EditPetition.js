import React, { useState } from "react";
import { connect } from "react-redux";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import { updatePetition } from "frontend/src/actions/petitions";

/**
 * Form for adding a new petition
 */
export const EditPetitionForm = (props) => {
  const {
    setPetitionType,
    setOrganization,
    setAttorneyName,
    setStreetAddress,
    setCity,
    setPhone,
    setBarId,
    setIFPMessage,
    setCrimHistReport,
  } = props;

  const {
    id,
    attorney = {},
    petition_type,
    ifp_message,
    include_crim_hist_report,
  } = props.petition;

  const handleSetPetitionType = (e) => {
    setPetitionType(e.target.value);
  };

  const handleSetOrganization = (e) => {
    setOrganization(e.target.value);
  };

  const handleSetAttorneyName = (e) => {
    setAttorneyName(e.target.value);
  };

  const handleSetStreetAddress = (e) => {
    setStreetAddress(e.target.value);
  };

  const handleSetCity = (e) => {
    setCity(e.target.value);
  };

  const handleSetPhone = (e) => {
    setPhone(e.target.value);
  };

  const handleSetBarId = (e) => {
    setBarId(e.target.value);
  };

  const handleSetIFPMessage = (e) => {
    setIFPMessage(e.target.value);
  };

  const handleSetCrimHistReport = (e) => {
    setCrimHistReport(e.target.value);
  };

  return (
    <form id={`edit-petition-${id}`}>
      <h3>
        Edit Petition <b>{id}</b>
      </h3>
      <div>
        <InputLabel id="petition-type">Petition Type</InputLabel>
        <Select
          labelId="petition-type"
          id="select-petition-type"
          value={petition_type}
          onChange={handleSetPetitionType}
        >
          <MenuItem value={"Expungement"}>Expungement</MenuItem>
          <MenuItem value={"Sealing"}>Sealing</MenuItem>
        </Select>
      </div>
      <h4> Attorney: </h4>
      <div>
        <div>
          <TextField
            label="Organization"
            value={attorney.organization}
            onChange={handleSetOrganization}
          />
          <TextField
            label="Full Name"
            value={attorney.full_name}
            onChange={handleSetAttorneyName}
          />
          <TextField
            label="Organization Address"
            value={
              attorney.organization_address
                ? attorney.organization_address.line_one
                : ""
            }
            onChange={handleSetStreetAddress}
          />
          <TextField
            label="Organization City/State/Zip"
            defaultValue={
              attorney.organization_address
                ? attorney.organization_address.city_state_zip
                : ""
            }
            onChange={handleSetCity}
          />
          <TextField
            label="Organization Phone"
            value={attorney.organization_phone || ""}
            onChange={handleSetPhone}
          />
          <TextField
            label="Bar ID number"
            value={attorney.bar_id || ""}
            onChange={handleSetBarId}
          />
        </div>
        <h4>Extras</h4>
        <div>
          <TextField
            label="IFP Message"
            value={ifp_message || ""}
            onChange={handleSetIFPMessage}
          />
          <TextField
            label="Crim. Hist. report included message?"
            value={include_crim_hist_report || ""}
            onChange={handleSetCrimHistReport}
          />
        </div>
        <Button type="submit">Done editing</Button>
      </div>
    </form>
  );
};

const mapStateToProps = (state, ownProps) => {
  console.log("mapping props");
  console.log(ownProps);
  const { petitionId } = ownProps;
  const petition =
    state.petitions.petitionCollection.entities.petitions[petitionId];
  console.log("petition");
  console.log(petition);
  return {
    petition: petition,
  };
};

const mapDispatchToProps = (dispatch, ownProps) => {
  const { petitionId } = ownProps;
  return {
    setPetitionType: (newType) =>
      dispatch(updatePetition(petitionId, { petition_type: newType })),
    setOrganization: (newOrg) => {
      dispatch(
        updatePetition(petitionId, { attorney: { organization: newOrg } })
      );
    },
    setAttorneyName: (newName) => {
      dispatch(
        updatePetition(petitionId, { attorney: { full_name: newName } })
      );
    },
    setStreetAddress: (newAddress) => {
      dispatch(
        updatePetition(petitionId, {
          attorney: { organization_address: { line_one: newAddress } },
        })
      );
    },
    setCity: (newCity) => {
      dispatch(
        updatePetition(petitionId, {
          attorney: { organization_address: { city_state_zip: newCity } },
        })
      );
    },
    setPhone: (newPhone) => {
      dispatch(
        updatePetition(petitionId, {
          attorney: { organization_phone: newPhone },
        })
      );
    },
    setBarId: (barId) => {
      dispatch(updatePetition(petitionId, { attorney: { bar_id: barId } }));
    },
    setIFPMessage: (message) => {
      dispatch(updatePetition(petitionId, { ifp_message: message }));
    },
    setCrimHistReport: (message) => {
      dispatch(
        updatePetition(petitionId, { include_crim_hist_report: message })
      );
    },
  };
};

export const EditPetitionFormConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(EditPetitionForm);
