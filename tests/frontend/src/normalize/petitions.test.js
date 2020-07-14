/**
 * Tests for normalizing petitions
 */
import {
  normalizePetitions,
  denormalizePetitions,
} from "frontend/src/normalize/petitions";
describe("normaizing and denormalizing a list of petitions.", () => {
  const petitionsFromServer = [
    {
      id: "1",
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
          charges: [
            {
              statute: "endangering othrs.",
            },
          ],
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

  test("normalize a list of petitions", () => {
    const normalized = normalizePetitions(petitionsFromServer);
    expect(normalized).toEqual({
      entities: {
        charges: {
          "12-CP-12-CR-1234567charges@0": {
            statute: "endangering othrs.",
            id: "12-CP-12-CR-1234567charges@0",
          },
        },
        cases: {
          "12-CP-12-CR-1234567": {
            docket_number: "12-CP-12-CR-1234567",
            affiant: "John",
            status: "closed",
            county: "Montgomery",
            charges: ["12-CP-12-CR-1234567charges@0"],
            id: "12-CP-12-CR-1234567",
            editing: false,
          },
        },
        petitions: {
          "1": {
            id: "1",
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
            client: {
              first_name: "Suzy",
              last_name: "Smith",
            },
            cases: ["12-CP-12-CR-1234567"],
            expungement_type: "FULL_EXPUNGEMENT",
            petition_type: "Expungment",
            summary_expuntement_language:
              "and Petitioner is over 70 years old and has been free of arrest for more than ten years since this summary conviction.",
            service_agencies: ["The Zoo", "Jims Pizza Palace"],
            include_crim_hist_report: "",
            ifp_message: "Please allow this petition.",
          },
        },
      },
      result: ["1"],
    });
  });
});

describe("denormalizing petitions", () => {
  const petitionsFromServer = [
    {
      id: "1",
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
          id: "12-CP-12-CR-1234567",
          editing: false,
          docket_number: "12-CP-12-CR-1234567",
          affiant: "John",
          status: "closed",
          county: "Montgomery",
          charges: [
            {
              id: "12-CP-12-CR-1234567charges@0",
              statute: "endangering othrs.",
            },
          ],
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

  // the way that petitions are stored in state:
  const petitionsInState = {
    state: {
      petitions: {
        petitionCollection: {
          petitionIds: ["1"],
          entities: {
            charges: {
              "12-CP-12-CR-1234567charges@0": {
                statute: "endangering othrs.",
                id: "12-CP-12-CR-1234567charges@0",
              },
            },
            cases: {
              "12-CP-12-CR-1234567": {
                docket_number: "12-CP-12-CR-1234567",
                affiant: "John",
                status: "closed",
                county: "Montgomery",
                charges: ["12-CP-12-CR-1234567charges@0"],
                id: "12-CP-12-CR-1234567",
                editing: false,
              },
            },
            petitions: {
              "1": {
                id: "1",
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
                client: {
                  first_name: "Suzy",
                  last_name: "Smith",
                },
                cases: ["12-CP-12-CR-1234567"],
                expungement_type: "FULL_EXPUNGEMENT",
                petition_type: "Expungment",
                summary_expuntement_language:
                  "and Petitioner is over 70 years old and has been free of arrest for more than ten years since this summary conviction.",
                service_agencies: ["The Zoo", "Jims Pizza Palace"],
                include_crim_hist_report: "",
                ifp_message: "Please allow this petition.",
              },
            },
          },
        },
      },
    },
  };

  test("denormalize a group of petitions.", () => {
    const denormalized = denormalizePetitions(
      petitionsInState.state.petitions.petitionCollection.petitionIds,
      petitionsInState.state.petitions.petitionCollection.entities
    );
    expect(denormalized).toEqual(petitionsFromServer);
  });
});
