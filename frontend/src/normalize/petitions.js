import { normalize, schema } from "normalizr";
import { caseSchema } from "./cases";

const petitionSchema = new schema.Entity("petitions", {
  cases: [caseSchema],
});

const petitionListSchema = new schema.Array(petitionSchema);

export const normalizePetitions = (petitions) => {
  const normalized = normalize(petitions, petitionListSchema);
  return normalized;
};
