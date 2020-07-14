import { normalize, schema, denormalize } from "normalizr";
import { caseSchema } from "./cases";

const petitionSchema = new schema.Entity("petitions", {
  cases: [caseSchema],
});

export const normalizeOnePetition = (petition, newId) => {
  petition.id = newId;
  return normalize(petition, petitionSchema);
};

const petitionListSchema = new schema.Array(petitionSchema);

export const normalizePetitions = (petitions) => {
  const normalized = normalize(petitions, petitionListSchema);
  return normalized;
};

export const denormalizePetitions = (petitionIds, entities) => {
  const denormalized = denormalize(petitionIds, petitionListSchema, entities);
  return denormalized;
};
