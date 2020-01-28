import React, { Component } from "react";
import {
  Container,
  Button,
  Modal,
  Icon,
  Grid,
  Divider,
  Form,
  Checkbox
} from "semantic-ui-react";

import {
  newViewObjectPlaceholder,
  newJoinObjectPlaceholder,
  newConditionObjectPlaceholder
} from "../../constant/index";
import ObjectCreator from "./ObjectCreator";

export default class Phase3Container extends Component {
  constructor(props) {
    super(props);
    this.state = {
      whichObject: null, // VIEWS| JOINS | CONDITIONS,
      showNewViewsModal: false,
      showNewJoinsModal: false,
      showNewConditionsModal: false,

      showExportJSON: false,
      content: []
    };
  }

  createSomeObj = type => {
    const { whichObject } = this.state;
    if (whichObject == null) {
      this.setState({
        whichObject: type
      });
    }
    switch (type) {
      case "VIEWS":
        this.setState({
          showNewViewsModal: true
        });
        break;
      case "JOINS":
        this.setState({
          showNewJoinsModal: true
        });
        break;
      case "CONDITIONS":
        this.setState({
          showNewConditionsModal: true
        });
        break;
      default:
        break;
    }
    
  };

  opsPerformed = ({ type, data, ...detail }) => {
    switch (type) {
      case "add_attribute": {
        const { content } = this.state;
        let copydata = JSON.parse(JSON.stringify(content));
        copydata.forEach(item => {
          if (item.alias === detail.objID) {
            item.attributes.push(data);
          }
        });
        this.setState({
          content: copydata
        });
        break;
      }

      default:
        console.log(`shouldn't have come here`);
    }
  };

  createNewObject = () => {
    
    let { whichObject, content } = this.state;
    let newQueryObject = newViewObjectPlaceholder;
    switch (whichObject) {

      case "VIEWS":
        let newViewObject = newViewObjectPlaceholder;
        newViewObject.tableName = document.getElementById("tableName").value;
        newViewObject.columnName = document.getElementById("columnName").value;

        content.push(newViewObject);
        this.setState({
          showNewViewsModal: false,
          content
        });
        break;

      case "JOINS":
        let newJoinObject = newJoinObjectPlaceholder;
        newJoinObject.leftTableName = document.getElementById("leftTableName").value
        newJoinObject.leftColumnName = document.getElementById("leftColumnName").value
        newJoinObject.rightTableName = document.getElementById("rightTableName").value
        newJoinObject.rightColumnName = document.getElementById("rightColumnName").value
        newJoinObject.joinType = document.getElementById("joinType").value
        content.push(newJoinObject);
        this.setState({
          showNewJoinsModal: false,
          content
        });
        break;

      case "CONDITIONS":
        let newConditionObject = newConditionObjectPlaceholder;
        newConditionObject.logicalOperator = document.getElementById("logicalOperator").value
        newConditionObject.rules = []

        content.push(newConditionObject);
        this.setState({
          showNewConditionsModal: false,
          content
        });
        break;

      default:
        break;

    }
  };

  render() {
    const {
      whichObject,
      content,
      showExportJSON,
      showNewViewsModal,
      showNewJoinsModal,
      showNewConditionsModal,
    } = this.state;
    return (
      <Container fluid style={{ padding: "3em" }}>
        <Modal dimmer="blurring" size="small" open={showNewViewsModal}>
          <Modal.Header>New View Creation</Modal.Header>
          <Modal.Content>
            <Form>
              <Form.Field>
                <label>Enter Table Name</label>
                <input type="text" id="tableName" />
              </Form.Field>

              <Form.Field>
                <label>Enter Column Name</label>
                <input type="text" id="columnName" />
              </Form.Field>

            </Form>
          </Modal.Content>
          <Modal.Actions>
            <Button
              secondary
              onClick={e => {
                if (content.length === 0) {
                  this.setState({
                    whichObject: null
                  });
                }
                this.setState({
                    showNewViewsModal: false
                });
              }}
            >
              Cancel
            </Button>
            <Button primary onClick={this.createNewObject}>
              Create
            </Button>
          </Modal.Actions>
        </Modal>
        <Modal dimmer="blurring" size="small" open={showNewJoinsModal}>
          <Modal.Header>New Join Creation</Modal.Header>
          <Modal.Content>
            <Form>
              <Form.Field>
                <label>Left Table Name</label>
                <input type="text" id="leftTableName" />
              </Form.Field>

              <Form.Field>
                <label>Left  Column Name</label>
                <input type="text" id="leftColumnName" />
              </Form.Field>

              <Form.Field>
                <label>Right Table Name</label>
                <input type="text" id="rightTableName" />
              </Form.Field>

              <Form.Field>
                <label>Right Column Name</label>
                <input type="text" id="rightColumnName" />
              </Form.Field>

              <Form.Field>
                <label>Join Type</label>
                <input type="text" id="joinType" />
              </Form.Field>

            </Form>
          </Modal.Content>
          <Modal.Actions>
            <Button
              secondary
              onClick={e => {
                if (content.length === 0) {
                  this.setState({
                    whichObject: null
                  });
                }
                this.setState({
                    showNewJoinsModal: false
                });
              }}
            >
              Cancel
            </Button>
            <Button primary onClick={this.createNewObject}>
              Create
            </Button>
          </Modal.Actions>
        </Modal>
        <Modal dimmer="blurring" size="small" open={showNewConditionsModal}>
          <Modal.Header>New Join Creation</Modal.Header>
          <Modal.Actions>
            <Button
              secondary
              onClick={e => {
                if (content.length === 0) {
                  this.setState({
                    whichObject: null
                  });
                }
                this.setState({
                    showNewConditionsModal: false
                });
              }}
            >
              Cancel
            </Button>
            <Button primary onClick={this.createNewObject}>
              Create
            </Button>
          </Modal.Actions>
        </Modal><Modal dimmer="blurring" size="small" open={showExportJSON}>
          <Modal.Header>Export to a JSON file</Modal.Header>
          <Modal.Content>
            <Form>
              <Form.Field>
                <label>Enter Filename</label>
                <input
                  type="text"
                  name="export_filename"
                  id="export_filename"
                />
              </Form.Field>
            </Form>
          </Modal.Content>
          <Modal.Actions>
            <Button
              primary
              onClick={e => {
                var dataString =
                  "data:text/json;charset=utf-8," +
                  encodeURIComponent(
                    JSON.stringify({
                      type: whichObject,
                      objects: content
                    })
                  );

                var downloadAnchor = document.createElement("a");
                downloadAnchor.setAttribute("href", dataString);
                downloadAnchor.setAttribute(
                  "download",
                  document.getElementById("export_filename").value + ".json"
                );
                document.body.appendChild(downloadAnchor);
                downloadAnchor.click();
                downloadAnchor.remove();
                this.setState({
                  showExportJSON: false
                });
              }}
            >
              Download
            </Button>
          </Modal.Actions>
        </Modal>
        <Grid>
          <Grid.Row columns={4}>
            
            <Grid.Column>
              <Button
                primary
                onClick={() => this.createSomeObj("VIEWS")}
              >
                <Icon name="add" />
                Views
              </Button>
            </Grid.Column>

            <Grid.Column>
              <Button
                secondary
                onClick={() => this.createSomeObj("JOINS")}
              >
                <Icon name="add" />
                Joins
              </Button>
            </Grid.Column>

            <Grid.Column>
              <Button 
                secondary
                onClick={() => this.createSomeObj("CONDITIONS")}
              >
                <Icon name="add" />
                Conditions
              </Button>
            </Grid.Column>
            
            <Grid.Column floated="right">
              <Button
                color="red"
                disabled={content.length === 0}
                onClick={() => {
                  this.setState({
                    showExportJSON: true
                  });
                }}
              >
                <Icon name="download" />
                Export
              </Button>
            </Grid.Column>
          </Grid.Row>
          <Divider />
          <Grid.Row columns={3}>
            {content.map((item, idx) => (
              <ObjectCreator
                item={item}
                key={idx}
                objectType={whichObject}
                allContent={content}
                onOps={this.opsPerformed}
              />
            ))}
          </Grid.Row>
        </Grid>
      </Container>
    );
  }
}
