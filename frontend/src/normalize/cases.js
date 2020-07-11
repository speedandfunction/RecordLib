import { normalize, denormalize, schema } from "normalizr";

/**
 * This gives each object in the normalized data a unique id.
 * @param  {Object} value  the object needing an id
 * @param  {Object} parent the object containing value
 * or containing the array which holds value
 * (or value itself if there is no containing object)
 * @param  {string | null} key    if present, the key for the field
 * within parent containing value (possibly as an item in an array)
 * @return {string}        the unique id
 */
const generateId = (value, parent, key) => {
  // Cases use their docket number as id.
  if (value.docket_number) return value.docket_number;
  // Defendants use their last name as id.
  if (value.last_name) return value.last_name;
  if (!key) return "root";

  // An object in an array starts with the parent's id,
  // then appends the key of the array containing the object
  // and then the object's index in the array.
  const index = parent[key].indexOf(value);
  return `${parent.id}${key}@${index}`;
};

/**
 * options passed to normalizr
 * Note, we are computing the same id twice,
 * because of how normalizr works (I think),
 * since we don't want to mutate the original data.
 * See for example https://stackoverflow.com/questions/39681284/normalizr-how-to-generate-slug-id-related-to-parent-entity
 * @type {Object}
 */
const options = {
  // copy an entity and add an id
  processStrategy: (value, parent, key) => {
    const newValue = Object.assign({}, value, {
      id: generateId(value, parent, key),
    });
    if (key === "cases") {
      newValue.editing = false;
    }

    return newValue;
  },
  idAttribute: (value, parent, key) => {
    return generateId(value, parent, key);
  },
};

// Schema for the normalized CRecord.
const sentenceSchema = new schema.Entity("sentences", {}, options);
const chargeSchema = new schema.Entity(
  "charges",
  { sentences: [sentenceSchema] },
  options
);
export const caseSchema = new schema.Entity(
  "cases",
  { charges: [chargeSchema] },
  options
);

export function normalizeCases(data) {
  const caseCollection = new schema.Entity(
    "caseCollection",
    [caseSchema],
    options
  );
  const normalized = normalize(data, caseCollection);
  return normalized;
}
