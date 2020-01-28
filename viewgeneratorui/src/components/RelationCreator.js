import React, { Component } from "react";
import {
  Button,
  Header,
  Label,
  Segment,
  Divider,
  Form,
  Icon,
  Grid
} from "semantic-ui-react";

import {
  newAssociationPlaceholder,
  associationTypes,
  getCardinality,
  rightAssociationPlaceholder
} from "../constant/index";

export default class RelationCreator extends Component {
  constructor(props) {
    super(props);
    this.state = {
      newAssociation: newAssociationPlaceholder,
      rAssociationPlaceholder: rightAssociationPlaceholder
    };
  }
  render() {
    const {
      objectsAvailableForAssociation,
      objectType,
      existingAssociations,
      createAssociation,
      removeAssociation,
      localAttribute,
      parentName
    } = this.props;
    const { newAssociation, rAssociationPlaceholder } = this.state;
    const associationOption = associationTypes[objectType].map(i => ({
      key: i,
      value: i,
      text: i
    }));
    const objectOptions = objectsAvailableForAssociation.map(item => ({
      key: item.alias,
      value: item.alias,
      text: item.alias
    }));
    let objectAttributeOptions = objectsAvailableForAssociation.filter(
      i => i.alias === rAssociationPlaceholder.object.name
    )[0];
    if (rAssociationPlaceholder.object.name.length) {
      objectAttributeOptions = objectAttributeOptions.attributes.map(i => ({
        key: i.alias,
        value: i.alias,
        text: i.alias
      }));
    }

    const localAttributeOptions = localAttribute.map(i => ({
      key: i.alias,
      value: i.alias,
      text: i.alias
    }));

    let existingAssociationDOM = existingAssociations !== undefined &&
      existingAssociations.length != 0 && (
        <>
          <Segment.Group>
            {existingAssociations.map((_item, idx) => {
              return (
                <Segment key={idx} clearing>
                  <div>
                    <Label.Group>
                      <h4>
                        {_item.identifier}{" "}
                        <Button
                          icon="trash"
                          size="mini"
                          floated="right"
                          onClick={e => {
                            let tmp = JSON.parse(JSON.stringify(_item));
                            removeAssociation(tmp);
                          }}
                        />
                      </h4>
                      {_item.rightAssociation.map((__item, index) => {
                        return (
                          <Segment key={index}>
                            <span className="jesus">
                              <strong>
                                {__item.object.name} ->{" "}
                                {__item.object.attribute}
                              </strong>
                            </span>
                            <br />
                            <strong>Cardinality</strong>
                            <br />
                            Min : {__item.cardinality.min} <br />
                            Max : {__item.cardinality.max} <br />
                          </Segment>
                        );
                      })}
                    </Label.Group>
                  </div>
                </Segment>
              );
            })}
          </Segment.Group>
          <Divider />
        </>
      );
    const titleHelper = objectType === "table" ? "Relation" : "Mapping";
    return (
      <Form>
        <Header as="h3">{titleHelper}</Header>
        {existingAssociationDOM}
        <Grid>
          <Grid.Row columns={2}>
            <Grid.Column>
              <Form.Field inline>
                <label>{titleHelper} Type</label>
                <Form.Select
                  options={associationOption}
                  onChange={(e, data) => {
                    let temp = JSON.parse(JSON.stringify(newAssociation)),
                      tmp = JSON.parse(JSON.stringify(rAssociationPlaceholder));
                    temp.identifier = data.value;
                    temp.name = data.value;
                    tmp.cardinality = getCardinality(data.value);
                    this.setState({
                      newAssociation: temp,
                      rAssociationPlaceholder: tmp
                    });
                  }}
                />
              </Form.Field>
            </Grid.Column>
            <Grid.Column>
              {newAssociation.identifier.length != 0 && (
                <Form.Field inline>
                  <label>Object Alias</label>
                  <Form.Select
                    options={objectOptions}
                    onChange={(e, d) => {
                      let tmp = JSON.parse(
                        JSON.stringify(rAssociationPlaceholder)
                      );
                      tmp.object.name = d.value;
                      tmp.object.attribute = parentName;
                      this.setState({
                        rAssociationPlaceholder: tmp
                      });
                    }}
                  />
                </Form.Field>
              )}
            </Grid.Column>
          </Grid.Row>
          {objectType === "table" &&
            rAssociationPlaceholder.object.name.length !== 0 && (
              <Grid.Row columns={2}>
                <Grid.Column>
                  <Form.Field inline>
                    <label>Local Attribute</label>
                    <Form.Select
                      options={localAttributeOptions}
                      onChange={(e, d) => {
                        let tmp = JSON.parse(
                          JSON.stringify(rAssociationPlaceholder)
                        );
                        tmp.object.localAttribute = d.value;
                        this.setState({
                          rAssociationPlaceholder: tmp
                        });
                      }}
                    />
                  </Form.Field>
                </Grid.Column>
                <Grid.Column>
                  <Form.Field inline>
                    <label>Attribute</label>
                    <Form.Select
                      options={objectAttributeOptions}
                      onChange={(e, d) => {
                        let tmp = JSON.parse(
                          JSON.stringify(rAssociationPlaceholder)
                        );
                        tmp.object.attribute = d.value;
                        this.setState({
                          rAssociationPlaceholder: tmp
                        });
                      }}
                    />
                  </Form.Field>
                </Grid.Column>
              </Grid.Row>
            )}

          {rAssociationPlaceholder.object.name.length !== 0 && (
            <>
              <Grid.Row columns={2}>
                <Grid.Column>
                  <Form.Field>
                    <label>
                      <strong>Cardinality</strong> Min
                    </label>
                    <Form.Input
                      placeholder="Min"
                      type="text"
                      value={rAssociationPlaceholder.cardinality.min}
                    />
                  </Form.Field>
                </Grid.Column>
                <Grid.Column>
                  <Form.Field>
                    <label>
                      <strong>Cardinality</strong> Max
                    </label>
                    <Form.Input
                      placeholder="Max"
                      type="text"
                      value={rAssociationPlaceholder.cardinality.max}
                    />
                  </Form.Field>
                </Grid.Column>
              </Grid.Row>
              <Grid.Row>
                <Grid.Column>
                  <Form.Button
                    primary
                    type="submit"
                    onClick={() => {
                      let tmp = JSON.parse(JSON.stringify(newAssociation));
                      tmp.rightAssociation.push(rAssociationPlaceholder);
                      createAssociation(tmp);
                      this.setState({
                        newAssociation: newAssociationPlaceholder,
                        rAssociationPlaceholder: rightAssociationPlaceholder
                      });
                    }}
                    title="add Association"
                  >
                    <Icon name="add" /> Create Association
                  </Form.Button>
                </Grid.Column>
              </Grid.Row>
            </>
          )}
        </Grid>
      </Form>
    );
  }
}
