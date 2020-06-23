const { integrateDocsWithRecord } = require("../../../../frontend/src/api");
import { normalizeCRecord } from "frontend/src/normalize";
import * as actions from "frontend/src/actions/crecord";
import cRecordReducer, {
  initialCrecordState,
} from "frontend/src/reducers/crecord";

describe("updating crecords", () => {
  it("updates state by normalizing a crecord returned from the server.", () => {
    const returnedCRecord = {
      person: {
        first_name: "john",
        last_name: "smith",
        date_of_birth: "2020-01-01",
      },
      cases: [
        {
          docket_number: "12-CP-12-CR-1234567",
          affiant: "John",
          status: "closed",
          county: "Montgomery",
          charges: [{ statute: "endangering othrs." }],
        },
      ],
    };

    const updateAction = actions.updateCRecordSucceeded(returnedCRecord);
    const newState = cRecordReducer(initialCrecordState, updateAction);
    expect(newState).toEqual({
      charges: {
        "12-CP-12-CR-1234567charges@0": {
          id: "12-CP-12-CR-1234567charges@0",
          statute: "endangering othrs.",
        },
      },
      cases: {
        "12-CP-12-CR-1234567": {
          id: "12-CP-12-CR-1234567",
          docket_number: "12-CP-12-CR-1234567",
          affiant: "John",
          editing: false,
          status: "closed",
          county: "Montgomery",
          charges: ["12-CP-12-CR-1234567charges@0"],
        },
      },
      sentences: {},
      cRecord: { ["root"]: { cases: ["12-CP-12-CR-1234567"] } },
    });
  });
});
