import React, { useState } from "react";
import { connect } from "react-redux";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import {
  updatePetition,
  setPetitionToEdit,
  newCaseForPetition,
} from "frontend/src/actions/petitions";
import { pickBy, pick } from "lodash";
/**
 * Form for adding a new petition
 */
export const EditPetitionForm = (props) => {
  const {
    petition = {},
    petitionCases, // obj of cases attached to this petition.
    petitionCaseIds, // convenience list of ids of cases attached to this petition.
    cases,
    charges,
    setPetitionType,
    setOrganization,
    setAttorneyName,
    setStreetAddress,
    setCity,
    setPhone,
    setBarId,
    setIFPMessage,
    setCrimHistReport,
    addCaseToPetition,
    setDoneEditing,
  } = props;

  const {
    id,
    attorney = {},
    petition_type,
    ifp_message,
    include_crim_hist_report,
  } = petition;

  // All the cases in the CRecord, so the user
  // can pick which ones to add to petitions.
  const caseIds = cases ? Object.keys(cases) : [];

  const [newCaseDocketNumber, setNewCaseDocketNumber] = useState("");

  // State hook to control the value of the new docket number to be added to this petition.
  const handleNewCaseDocketNumChange = (e) => {
    setNewCaseDocketNumber(e.target.value);
  };

  // Dispatch action to copy a case from crecord into Petition state.
  const handleAddCaseToPetition = (e) => {
    e.preventDefault();
    console.log("handling add case button");
    const caseInfo = cases[newCaseDocketNumber];
    console.log(caseInfo);
    const chargesToAdd = pick(charges, caseInfo.charges);
    console.log(chargesToAdd);
    console.log("now dispatching.");
    addCaseToPetition(newCaseDocketNumber, caseInfo, chargesToAdd);
    setNewCaseDocketNumber("");
  };

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

  const handleDoneEditing = (e) => {
    setDoneEditing();
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
            value={attorney.address ? attorney.address.line_one : ""}
            onChange={handleSetStreetAddress}
          />
          <TextField
            label="Organization City/State/Zip"
            defaultValue={
              attorney.address ? attorney.address.city_state_zip : ""
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
        <h4>Messages</h4>
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
        <h4>Cases</h4>
        <div>
          <InputLabel id="case-select-label">Add a case</InputLabel>
          <Select
            labelId="case-select-label"
            id="case-select"
            value={newCaseDocketNumber}
            onChange={handleNewCaseDocketNumChange}
          >
            {caseIds.map((caseId) => {
              return (
                <MenuItem key={caseId} value={caseId}>
                  {caseId}
                </MenuItem>
              );
            })}
          </Select>
        </div>
        <div>
          <ul>
            {petitionCaseIds.map((pid) => {
              return (
                <li key={pid}>
                  Docket Number: {petitionCases[pid].docket_number}{" "}
                </li>
              );
            })}
          </ul>
        </div>
        <Button
          onClick={handleAddCaseToPetition}
          disabled={newCaseDocketNumber === ""}
        >
          Add new case to petition
        </Button>
      </div>
      <Button type="submit" onClick={handleDoneEditing}>
        Done editing
      </Button>
    </form>
  );
};

const mapStateToProps = (state, ownProps) => {
  const { petitionId } = ownProps;
  const petition =
    state.petitions.petitionCollection.entities.petitions[petitionId];
  const petitionCaseIds = petition.cases || [];
  const petitionCases = pickBy(
    state.petitions.petitionCollection.entities.cases,
    (val, key) => {
      return petitionCaseIds.includes(key);
    }
  );
  const cases = state.crecord.cases;
  return {
    petition: petition,
    petitionCases: petitionCases,
    petitionCaseIds: petitionCaseIds,
    cases: cases,
    charges: state.crecord.charges,
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
    addCaseToPetition: (caseId, caseInfo, chargeInfo) => {
      dispatch(newCaseForPetition(petitionId, caseId, caseInfo, chargeInfo));
    },
    setDoneEditing: () => {
      dispatch(setPetitionToEdit(null));
    },
  };
};

export const EditPetitionFormConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(EditPetitionForm);
