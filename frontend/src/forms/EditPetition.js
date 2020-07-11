import React, { useState } from "react";
import { connect } from "react-redux";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
/**
 * Form for adding a new petition
 */

export const EditPetitionForm = (props) => {
  const {
    petitionId,
    attorney = {},
    petition_type,
    ifp_message,
    include_crim_hist_report,
  } = props;

  const [selectedPetitionType, setPetitionType] = useState(
    petition_type || "Expungement"
  );

  const handleSetPetitionType = (e) => {
    setPetitionType(e.target.value);
  };

  return (
    <form id={`edit-petition-${petitionId}`}>
      <h3>
        Edit Petition <b>{petitionId}</b>
      </h3>
      <div>
        <InputLabel id="petition-type">Petition Type</InputLabel>
        <Select
          labelId="petition-type"
          id="select-petition-type"
          value={selectedPetitionType}
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
            defaultValue={attorney.organization || ""}
          />
          <TextField
            label="Full Name"
            defaultValue={attorney.full_name || ""}
          />
          <TextField
            label="Organization Address"
            defaultValue={
              attorney.organization_address
                ? attorney.organization_address.line_one || ""
                : ""
            }
          />
          <TextField
            label="Organization City/State/Zip"
            defaultValue={
              attorney.organization_address
                ? attorney.organization_address.city_state_zip || ""
                : ""
            }
          />
          <TextField
            label="Organization Phone"
            defaultValue={attorney.organization_phone || ""}
          />
          <TextField label="BarID" defaultValue={attorney.bar_id || ""} />
        </div>
        <h4>Extras</h4>
        <div>
          <TextField label="IFP Message" defaultValue={ifp_message || ""} />
          <TextField
            label="Crim. Hist. report included message?"
            defaultValue={include_crim_hist_report || ""}
          />
        </div>
        <Button type="submit">Done editing</Button>
      </div>
    </form>
  );
};

const mapStateToProps = (state) => {
  return {};
};

export const EditPetitionFormConnected = connect(mapStateToProps)(
  EditPetitionForm
);
