const { TestScheduler } = require("jest");
import petitionsReducer, {
  petitionCollectionReducer,
} from "frontend/src/reducers/petitions";
import {
  newPetition,
  updatePetition,
  newCaseForPetition,
} from "frontend/src/actions/petitions";

describe("slice of state for the petitionCollection", () => {
  test("initial state", () => {
    expect(petitionsReducer(undefined, {})).toEqual({
      petitionUpdates: { updateInProgress: false },
      petitionCollection: {
        entities: {
          petitions: {},
          cases: {},
          charges: {},
        },
        petitionIds: [],
        editingPetitionId: null,
      },
    });
  });

  test("add new petitions from server", () => {
    const petitionsFromServer = [
      {
        attorney: {
          organization: "Legal Aid Org",
          full_name: "Abraham Lincoln",
          organization_address: {
            line_one: "1234 S. St.",
            city_state_zip: "Phila PA",
          },
          organization_phone: "123-123-1234",
          bar_id: "11222",
        },
        client: { first_name: "Suzy", last_name: "Smith" },
        cases: [
          {
            docket_number: "12-CP-12-CR-1234567",
            affiant: "John",
            status: "closed",
            county: "Montgomery",
            charges: [{ statute: "endangering othrs." }],
          },
        ],
        expungement_type: "FULL_EXPUNGEMENT",
        petition_type: "Expungment", // as opposed to "Sealing",
        summary_expuntement_language:
          "and Petitioner is over 70 years old and has been free of arrest for more than ten years since this summary conviction.",
        service_agencies: ["The Zoo", "Jims Pizza Palace"],
        include_crim_hist_report: "",
        ifp_message: "Please allow this petition.",
      },
    ];

    const newState = petitionsReducer(
      undefined,
      newPetition(petitionsFromServer[0])
    );

    expect(newState).toEqual({
      petitionUpdates: { updateInProgress: false },
      petitionCollection: {
        entities: {
          petitions: {
            "0": {
              id: "0",
              attorney: {
                organization: "Legal Aid Org",
                full_name: "Abraham Lincoln",
                organization_address: {
                  line_one: "1234 S. St.",
                  city_state_zip: "Phila PA",
                },
                organization_phone: "123-123-1234",
                bar_id: "11222",
              },
              client: { first_name: "Suzy", last_name: "Smith" },
              cases: ["12-CP-12-CR-1234567"],
              expungement_type: "FULL_EXPUNGEMENT",
              petition_type: "Expungment", // as opposed to "Sealing",
              summary_expuntement_language:
                "and Petitioner is over 70 years old and has been free of arrest for more than ten years since this summary conviction.",
              service_agencies: ["The Zoo", "Jims Pizza Palace"],
              include_crim_hist_report: "",
              ifp_message: "Please allow this petition.",
            },
          },
          cases: {
            "12-CP-12-CR-1234567": {
              id: "12-CP-12-CR-1234567",
              docket_number: "12-CP-12-CR-1234567",
              affiant: "John",
              status: "closed",
              county: "Montgomery",
              charges: ["12-CP-12-CR-1234567charges@0"],
              editing: false,
            },
          },
          charges: {
            "12-CP-12-CR-1234567charges@0": {
              id: "12-CP-12-CR-1234567charges@0",
              statute: "endangering othrs.",
            },
          },
        },
        petitionIds: ["0"],
        editingPetitionId: "0",
      },
    });
  });

  test("add new case to a petition", () => {
    /**
     * we need to be able to add a new case to a petition.
     * this reducer will need to take a petitionID and the id of a new case to tie to that petition.
     *
     * The reducer will need to append that new case id to the list of cases in the given petition.
     * And it will need to to create at least a key w/ empty object in the entities.cases collection.
     */
    const startingState = {
      petitionUpdates: { updateInProgress: false },
      petitionCollection: {
        editingPetitionId: "0",
        entities: {
          petitions: {
            "0": {
              id: "0",
              attorney: {
                organization: "Legal Aid Org",
                full_name: "Abraham Lincoln",
                organization_address: {
                  line_one: "1234 S. St.",
                  city_state_zip: "Phila PA",
                },
                organization_phone: "123-123-1234",
                bar_id: "11222",
              },
              client: { first_name: "Suzy", last_name: "Smith" },
              cases: ["12-CP-12-CR-1234567"],
              expungement_type: "FULL_EXPUNGEMENT",
              petition_type: "Expungment", // as opposed to "Sealing",
              summary_expuntement_language:
                "and Petitioner is over 70 years old and has been free of arrest for more than ten years since this summary conviction.",
              service_agencies: ["The Zoo", "Jims Pizza Palace"],
              include_crim_hist_report: "",
              ifp_message: "Please allow this petition.",
            },
          },
          cases: {
            "12-CP-12-CR-1234567": {
              id: "12-CP-12-CR-1234567",
              docket_number: "12-CP-12-CR-1234567",
              affiant: "John",
              status: "closed",
              county: "Montgomery",
              charges: ["12-CP-12-CR-1234567charges@0"],
              editing: false,
            },
          },
          charges: {
            "12-CP-12-CR-1234567charges@0": {
              id: "12-CP-12-CR-1234567charges@0",
              statute: "endangering othrs.",
            },
          },
        },
        petitionIds: ["0"],
      },
    };

    const updateAction = newCaseForPetition("0", "20-CP-20-CR-1234567");
    const modifiedState = petitionsReducer(startingState, updateAction);
    expect(modifiedState).toEqual({
      petitionUpdates: { updateInProgress: false },
      petitionCollection: {
        editingPetitionId: "0",
        entities: {
          petitions: {
            "0": {
              id: "0",
              attorney: {
                organization: "Legal Aid Org",
                full_name: "Abraham Lincoln",
                organization_address: {
                  line_one: "1234 S. St.",
                  city_state_zip: "Phila PA",
                },
                organization_phone: "123-123-1234",
                bar_id: "11222",
              },
              client: { first_name: "Suzy", last_name: "Smith" },
              cases: ["12-CP-12-CR-1234567", "20-CP-20-CR-1234567"],
              expungement_type: "FULL_EXPUNGEMENT",
              petition_type: "Expungment", // as opposed to "Sealing",
              summary_expuntement_language:
                "and Petitioner is over 70 years old and has been free of arrest for more than ten years since this summary conviction.",
              service_agencies: ["The Zoo", "Jims Pizza Palace"],
              include_crim_hist_report: "",
              ifp_message: "Please allow this petition.",
            },
          },
          cases: {
            "12-CP-12-CR-1234567": {
              id: "12-CP-12-CR-1234567",
              docket_number: "12-CP-12-CR-1234567",
              affiant: "John",
              status: "closed",
              county: "Montgomery",
              charges: ["12-CP-12-CR-1234567charges@0"],
              editing: false,
            },
            "20-CP-20-CR-1234567": {
              id: "20-CP-20-CR-1234567",
              docket_number: "20-CP-20-CR-1234567",
              editing: false,
            },
          },
          charges: {
            "12-CP-12-CR-1234567charges@0": {
              id: "12-CP-12-CR-1234567charges@0",
              statute: "endangering othrs.",
            },
          },
        },
        petitionIds: ["0"],
      },
    });
  });

  test("update a petition", () => {
    const startingState = {
      petitionUpdates: { updateInProgress: false },
      petitionCollection: {
        editingPetitionId: "0",
        entities: {
          petitions: {
            "0": {
              id: "0",
              attorney: {
                organization: "Legal Aid Org",
                full_name: "Abraham Lincoln",
                organization_address: {
                  line_one: "1234 S. St.",
                  city_state_zip: "Phila PA",
                },
                organization_phone: "123-123-1234",
                bar_id: "11222",
              },
              client: { first_name: "Suzy", last_name: "Smith" },
              cases: ["12-CP-12-CR-1234567"],
              expungement_type: "FULL_EXPUNGEMENT",
              petition_type: "Expungment", // as opposed to "Sealing",
              summary_expuntement_language:
                "and Petitioner is over 70 years old and has been free of arrest for more than ten years since this summary conviction.",
              service_agencies: ["The Zoo", "Jims Pizza Palace"],
              include_crim_hist_report: "",
              ifp_message: "Please allow this petition.",
            },
          },
          cases: {
            "12-CP-12-CR-1234567": {
              id: "12-CP-12-CR-1234567",
              docket_number: "12-CP-12-CR-1234567",
              affiant: "John",
              status: "closed",
              county: "Montgomery",
              charges: ["12-CP-12-CR-1234567charges@0"],
              editing: false,
            },
          },
          charges: {
            "12-CP-12-CR-1234567charges@0": {
              id: "12-CP-12-CR-1234567charges@0",
              statute: "endangering othrs.",
            },
          },
        },
        petitionIds: ["0"],
      },
    };

    // now update this starting state with update action.

    const updateAction = updatePetition("0", {
      attorney: { organization: "New Org" },
    });
    const newState = petitionsReducer(startingState, updateAction);
    expect(newState).toEqual({
      petitionUpdates: { updateInProgress: false },
      petitionCollection: {
        editingPetitionId: "0",
        entities: {
          petitions: {
            "0": {
              id: "0",
              attorney: {
                organization: "New Org",
                full_name: "Abraham Lincoln",
                organization_address: {
                  line_one: "1234 S. St.",
                  city_state_zip: "Phila PA",
                },
                organization_phone: "123-123-1234",
                bar_id: "11222",
              },
              client: { first_name: "Suzy", last_name: "Smith" },
              cases: ["12-CP-12-CR-1234567"],
              expungement_type: "FULL_EXPUNGEMENT",
              petition_type: "Expungment", // as opposed to "Sealing",
              summary_expuntement_language:
                "and Petitioner is over 70 years old and has been free of arrest for more than ten years since this summary conviction.",
              service_agencies: ["The Zoo", "Jims Pizza Palace"],
              include_crim_hist_report: "",
              ifp_message: "Please allow this petition.",
            },
          },
          cases: {
            "12-CP-12-CR-1234567": {
              id: "12-CP-12-CR-1234567",
              docket_number: "12-CP-12-CR-1234567",
              affiant: "John",
              status: "closed",
              county: "Montgomery",
              charges: ["12-CP-12-CR-1234567charges@0"],
              editing: false,
            },
          },
          charges: {
            "12-CP-12-CR-1234567charges@0": {
              id: "12-CP-12-CR-1234567charges@0",
              statute: "endangering othrs.",
            },
          },
        },
        petitionIds: ["0"],
      },
    });
  });
});
