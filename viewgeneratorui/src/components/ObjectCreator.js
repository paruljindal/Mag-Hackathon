import React, { Component } from "react";
import {
  Button,
  Grid,
  Confirm,
  Header,
  Label,
  Divider,
  Segment,
  Form,
  Checkbox,
  Icon
} from "semantic-ui-react";

import {
  newAttributePlaceholder,
  newAssociationPlaceholder,
  specifierOptions
} from "../constant/index";
import RelationCreator from "./RelationCreator";

export default class ObjectCreator extends Component {
  constructor(props) {
    super(props);
    this.state = {
      duplicateFound: false,
      attribute: newAttributePlaceholder,
      associations: newAssociationPlaceholder
    };
  }

  createAssociation = data => {
    // let tmp = this.state.associations;
    // tmp.rightAssociation.push(data);
    this.props.onOps({
      type: "add_association",
      objID: this.props.item.alias,
      association: {
        identifier: data.identifier,
        rightAssociation: data.rightAssociation
      }
    });
  };

  removeAssociation = data => {
    let tmp = this.state.associations;
    tmp.rightAssociation.push(data);
    this.props.onOps({
      type: "rem_association",
      objID: this.props.item.alias,
      association: data
    });
  };

  render() {
    const { item, onOps, objectType, allContent, advancedView } = this.props;
    const { attribute, duplicateFound } = this.state;
    let { alias, type, ...rest } = attribute;
    const objectsAvailableForAssociation = allContent.filter(
      _item => _item.alias !== item.alias
    );
    const localObjectAttributes = item.attributes;
    const aliases = item.attributes.map(i => {
      return i.alias;
    });
    const dataTypeOptions = [
      { key: "String", value: "String", text: "String" },
      { key: "Integer", value: "Integer", text: "Integer" }
    ];
    return (
      <Grid.Column>
        <Header attached="top" as="h4" inverted>
          {item.alias}
          <Button
            icon="close"
            basic
            size="small"
            floated="right"
            onClick={e => {
              onOps({
                type: "rem_object",
                objID: item.alias
              });
            }}
          />
        </Header>
        <Segment attached="bottom">
          <Segment.Group>
            {item.attributes.map(att => {
              return (
                <Segment key={att.alias} clearing>
                  <div>
                    <Label.Group tag>
                      {att.alias}
                      <Label as="a" style={{ marginLeft: "2em" }}>
                        {att.type}
                      </Label>
                      {objectType.toLowerCase() === "table" && att.isPrimary && (
                        <Label as="a" style={{ marginLeft: "2em" }}>
                          Primary Key
                        </Label>
                      )}
                      {objectType.toLowerCase() === "class" && att.specifier && (
                        <Label as="a" style={{ marginLeft: "2em" }}>
                          {att.specifier}
                        </Label>
                      )}
                      <Button
                        icon="trash"
                        size="small"
                        floated="right"
                        onClick={e => {
                          onOps({
                            type: "rem_attribute",
                            objID: item.alias,
                            data: {
                              object_att_alias: att.alias
                            }
                          });
                        }}
                      />
                    </Label.Group>
                  </div>
                </Segment>
              );
            })}
          </Segment.Group>
          <Divider />
          <Form>
            <Header as="h3">Attribute Creation</Header>
            <Form.Input
              // fluid
              placeholder="Attribute name"
              type="text"
              onChange={(e, data) => {
                let temp = JSON.parse(JSON.stringify(attribute));
                temp.alias = data.value;
                temp.name = data.value;
                this.setState({
                  attribute: temp
                });
              }}
              value={attribute.alias}
            />
            <Grid>
              <Grid.Row columns={2}>
                <Grid.Column>
                  {objectType.toLowerCase() === "table" && (
                    <Form.Field>
                      <label>Primary Key</label>
                      <Checkbox
                        // label="Primary Key"
                        onChange={(e, d) => {
                          let temp = JSON.parse(JSON.stringify(attribute));
                          temp.isPrimary = d.checked;
                          this.setState({
                            attribute: temp
                          });
                        }}
                      />
                    </Form.Field>
                  )}
                  {objectType.toLowerCase() === "class" && (
                    <Form.Field>
                      <label>Specifier</label>
                      <Form.Select
                        options={specifierOptions}
                        onChange={(e, d) => {
                          let temp = JSON.parse(JSON.stringify(attribute));
                          temp.specifier = d.value;
                          this.setState({
                            attribute: temp
                          });
                        }}
                      />
                    </Form.Field>
                  )}
                </Grid.Column>
                <Grid.Column>
                  <Form.Field>
                    <label>Data Type</label>
                    <Form.Select
                      options={dataTypeOptions}
                      value={type}
                      onChange={(e, data) => {
                        let temp = JSON.parse(JSON.stringify(attribute));
                        temp.type = data.value;
                        this.setState({
                          attribute: temp
                        });
                      }}
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
                      if (aliases.indexOf(alias) !== -1) {
                        this.setState({
                          duplicateFound: true
                        });
                      } else {
                        onOps({
                          type: "add_attribute",
                          objID: item.alias,
                          data: attribute
                        });
                        this.setState({
                          attribute: newAttributePlaceholder
                        });
                      }
                    }}
                    title="add attribute"
                    // icon="add"
                  >
                    <Icon name="add" /> Add Attribute
                  </Form.Button>
                </Grid.Column>
              </Grid.Row>
            </Grid>
          </Form>
          <Divider />
          {advancedView && (
            <RelationCreator
              objectsAvailableForAssociation={objectsAvailableForAssociation}
              localAttribute={localObjectAttributes}
              objectType={objectType}
              parentName={item.name}
              existingAssociations={item.associations}
              createAssociation={this.createAssociation}
              removeAssociation={this.removeAssociation}
            />
          )}
        </Segment>
        <Confirm
          content="Duplicate Attribute values found"
          open={duplicateFound}
          size="small"
          onCancel={() => this.setState({ duplicateFound: false })}
          onConfirm={() => this.setState({ duplicateFound: false })}
        />
      </Grid.Column>
    );
  }
}
