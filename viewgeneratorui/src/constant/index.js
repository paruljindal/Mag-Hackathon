export const APIEndpoint = `http://localhost:8000/`;

export const newObjectPlaceholder = {
  alias: "",
  name: "",
  attributes: [],
  associations: []
};

export const newQueryObjectPlaceholder = {
  views: [],
  joins: [],
  conditions: []
};

export const newViewObjectPlaceholder = {
  tableName: null,
  columnName: null
};

export const newJoinObjectPlaceholder = {
  leftTableName: null,
  leftColumnName: null,
  rightTableName: null,
  rightColumnName: null,
  joinType: null
};

export const newConditionObjectPlaceholder = {
  logicalOperator: null,
  rules: []
};

export const newAttributePlaceholder = {
  specifier: "",
  isPrimary: false,
  alias: "",
  name: "",
  type: ""
};

export const newAssociationPlaceholder = {
  identifier: "",
  rightAssociation: []
};

export const associationTypes = {
  table: ["OneToOne", "OneToMany", "ManyToOne", "ManyToMany"],
  class: ["AGGREGATION", "ASSOCIATION", "COMPOSITION", "INHERITANCE"]
};

export function getCardinality(associationType) {
  const cardinality = {
    OneToOne: {
      min: "1",
      max: "1"
    },
    OneToMany: {
      min: "1",
      max: "N"
    },
    ManyToOne: {
      min: "1",
      max: "N"
    },
    ManyToMany: {
      min: "N",
      max: "N"
    },
    AGGREGATION: {
      min: "1",
      max: "N"
    },
    ASSOCIATION: {
      min: "1",
      max: "N"
    },
    COMPOSITION: {
      min: "1",
      max: "N"
    },
    INHERITANCE: {
      min: "N/A",
      max: "N/A"
    }
  };
  return cardinality[associationType];
}

export const rightAssociationPlaceholder = {
  object: {
    name: "",
    attribute: "",
    localAttribute: "",
    isInsertRequired: false
  },
  cardinality: {
    min: "",
    max: ""
  }
};

export const specifierOptions = [
  { key: "Public", value: "Public", text: "Public" },
  { key: "Private", value: "Private", text: "Private" },
  { key: "Protected", value: "Protected", text: "Protected" }
];

export const joinTypes = ["FULL JOIN", "LEFT JOIN", "RIGHT JOIN", "INNER JOIN"];

export const logicalOperatorTypes = ["AND", "OR"];

export const comparisionOperatorTypes = ["LIKE", "EQ", "GT", "LT", "NEQ", "IN"];
