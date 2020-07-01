import {
  normalizeCRecord,
  denormalizeSourceRecords,
  normalizeCases,
} from "frontend/src/normalize";

describe("case normalizer", () => {
  it("normalize cases.", () => {
    const cases = [
      {
        docket_number: "12-CP-12-CR-1234567",
        affiant: "John",
        status: "closed",
        county: "Montgomery",
        charges: [{ statute: "endangering othrs." }],
      },
    ];

    const normalized = normalizeCases(cases);
    expect(normalized).toEqual({
      entities: {
        cases: {
          "12-CP-CR-1234567": {
            id: "12-CP-CR-1234567",
            docket_number: "12-CP-12-CR-1234567",
            affiant: "John",
            status: "closed",
            county: "Montgomery",
            charges: [1],
          },
        },
        charges: {
          1: {
            id: 1,
            statute: "endangering othrs.",
          },
        },
        sentences: {},
      },
      result: {
        cases: ["12-CP-CR-1234567"],
        charges: [1],
        sentences: [],
      },
    });
  });
});

describe("crecord normalizers", () => {
  it("should turn an empty crecord nested object into empty normalized components.", () => {
    const crecord = {
      cases: [],
    };
    const normalized = normalizeCRecord(crecord);
    expect(normalized).toEqual({
      entities: {
        cRecord: {
          root: {
            id: "root",
            cases: [],
          },
        },
      },
      result: "root",
    });
  });

  it("should normalize a crecord response from the server", () => {
    const crecord = {
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
    console.log("response normalized");
    const normalized = normalizeCRecord(crecord);
    console.log(normalized);
    console.log(normalized.entities.cRecord);
    expect(normalized).toEqual({
      entities: {
        cRecord: {
          root: {
            cases: ["12-CP-12-CR-1234567"],
            id: "root",
          },
        },
        cases: {
          "12-CP-12-CR-1234567": {
            docket_number: "12-CP-12-CR-1234567",
            editing: false,
            id: "12-CP-12-CR-1234567",
            affiant: "John",
            status: "closed",
            county: "Montgomery",
            charges: ["12-CP-12-CR-1234567charges@0"],
          },
        },
        charges: {
          "12-CP-12-CR-1234567charges@0": {
            id: "12-CP-12-CR-1234567charges@0",
            statute: "endangering othrs.",
          },
        },
      },
      result: "root",
    });
  });
});

describe("normalizing sourceRecords", () => {
  it("should denormalize from the normalized shape", () => {
    const normalized = {
      allIds: ["abc", "123"],
      allSourceRecords: {
        abc: {
          id: "abc",
          caption: "A v. B",
          court: "CP",
        },
        "123": {
          id: "123",
          caption: "1 v 2",
          court: "MD",
        },
      },
    };

    const denormalized = denormalizeSourceRecords(normalized);
    expect(denormalized).toEqual([
      {
        id: "abc",
        caption: "A v. B",
        court: "CP",
      },
      {
        id: "123",
        caption: "1 v 2",
        court: "MD",
      },
    ]);
  });
});
