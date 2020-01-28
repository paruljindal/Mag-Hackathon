import React, { Component } from "react";
import {
  Container,
  Button,
  Modal,
  Segment,
  Icon,
  Grid,
  Divider,
  Form,
  Checkbox
} from "semantic-ui-react";
import axios from "axios";

import { newObjectPlaceholder, APIEndpoint } from "../constant/index";
import ObjectCreator from "./ObjectCreator";

export default class BMContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      whichObject: null, // class|table|null
      showNewObjectModal: false,
      showExportJSON: false,
      showViewGenerator: false,
      content: [],
      advancedView: false,
      showUploadModal: false
    };
  }

  createSomeObj = type => {
    const { whichObject } = this.state;
    if (whichObject == null) {
      this.setState({
        whichObject: type
      });
    }
    this.setState({
      showNewObjectModal: true
    });
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

      case "rem_attribute": {
        const { content } = this.state;
        let copydata = JSON.parse(JSON.stringify(content));
        copydata.forEach(obj => {
          if (obj.alias === detail.objID) {
            obj.attributes = obj.attributes.filter(
              att => att.alias !== data.object_att_alias
            );
          }
        });
        this.setState({
          content: copydata
        });
        break;
      }

      case "rem_object": {
        const { content } = this.state;
        let copyData = JSON.parse(JSON.stringify(content));
        copyData = copyData.filter(obj => obj.alias !== detail.objID);
        if (copyData.length === 0) {
          this.setState({
            whichObject: null
          });
        }
        this.setState({
          content: copyData
        });
        break;
      }

      case "add_association": {
        const { content } = this.state;
        let copyData = JSON.parse(JSON.stringify(content));
        copyData.forEach(item => {
          if (item.alias === detail.objID) {
            let dirty = false;
            item.associations.forEach(_item => {
              if (_item.identifier === detail.association.identifier) {
                dirty = true;
                _item.rightAssociation.push(
                  // assumption that the RelationCreator only sends in an array containing only one object
                  detail.association.rightAssociation[0]
                );
              }
            });
            if (!dirty) {
              item.associations.push(detail.association);
            }
          }
        });

        this.setState({
          content: copyData
        });
        break;
      }

      case "rem_association": {
        const { content } = this.state;
        let copyData = JSON.parse(JSON.stringify(content));
        copyData.forEach(obj => {
          if (obj.alias === detail.objID) {
            obj.associations = obj.associations.filter(
              i => JSON.stringify(i) !== JSON.stringify(detail.association)
            );
          }
        });
        this.setState({
          content: copyData
        });
        break;
      }

      default:
        console.log(`shouldn't have come here`);
    }
  };

  createNewObject = () => {
    const objectName = document.getElementById("pooper").value;
    const { content } = this.state;
    let { whichObject } = this.state;
    let copyData = JSON.parse(JSON.stringify(content));
    let newshit = newObjectPlaceholder;
    newshit.alias = objectName;
    newshit.name = objectName;
    newshit.attributes = [];
    newshit.associations[whichObject] = [];
    copyData.push(newshit);
    this.setState({
      showNewObjectModal: false,
      content: copyData
    });
  };

  fetchJava = obj => {
    let url = `${APIEndpoint}getClasses/`;
    axios
      .post(url, JSON.stringify(obj), {
        headers: {
          "Content-Type": "application/zip"
        },
        responseType: "arraybuffer"
      })
      .then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "Export.zip"); //or any other extension
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      });
  };

  fetchSQL = obj => {
    let url = `${APIEndpoint}getSQL/`;
    axios
      .post(url, JSON.stringify(obj), {
        responseType: "text"
      })
      .then(res => {
        if (res.data.length == 0) {
          alert("unable to generate");
        } else {
          var element = document.createElement("a");
          element.setAttribute(
            "href",
            "data:text/plain;charset=utf-8," + encodeURIComponent(res.data)
          );
          element.setAttribute("download", "generated_file.sql");

          element.style.display = "none";
          document.body.appendChild(element);

          element.click();

          document.body.removeChild(element);
        }
      })
      .catch(err => {
        console.info(err);
      });
  };

  render() {
    const {
      whichObject,
      content,
      showExportJSON,
      showUploadModal,
      advancedView,
      showViewGenerator,
      showNewObjectModal
    } = this.state;
    return (
      <Container fluid style={{ padding: "3em" }}>
        <Modal dimmer="blurring" size="small" open={showNewObjectModal}>
          <Modal.Header>New Object Creation</Modal.Header>
          <Modal.Content>
            <Form>
              <Form.Field>
                <label>Enter Object Name</label>
                <input type="text" id="pooper" />
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
                  showNewObjectModal: false
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
        <Modal dimmer="blurring" size="small" open={showExportJSON}>
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
                const objects = JSON.parse(JSON.stringify(content));
                var dataString =
                  "data:text/json;charset=utf-8," +
                  encodeURIComponent(
                    JSON.stringify({
                      type: whichObject,
                      objects
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
        <Modal dimmer="blurring" size="small" open={showUploadModal}>
          <Modal.Header>Upload a JSON file</Modal.Header>
          <Modal.Content>
            <input name="file" id="uploadfile" type="file" />
          </Modal.Content>
          <Modal.Actions>
            <Button
              primary
              onClick={e => {
                let reader = new FileReader();
                const that = this;
                reader.onload = function(e) {
                  let obj = JSON.parse(e.target.result);
                  that.setState({
                    showUploadModal: false,
                    content: obj.objects,
                    whichObject: obj.type.toLowerCase()
                  });
                };
                reader.readAsText(
                  document.getElementById("uploadfile").files[0]
                );
              }}
            >
              Upload
            </Button>
          </Modal.Actions>
        </Modal>
        <Grid columns={3} divided>
          <Grid.Row stretched>
            <Grid.Column>
              <Segment>
                <Button
                  primary
                  disabled={whichObject && whichObject === "table"}
                  onClick={() => this.createSomeObj("class")}
                >
                  <Icon name="add" />
                  Class
                </Button>
                {/* </Segment>
                  <Segment> */}
                <Button
                  floated="right"
                  secondary
                  disabled={whichObject && whichObject === "class"}
                  onClick={() => this.createSomeObj("table")}
                >
                  <Icon name="add" />
                  Table
                </Button>
              </Segment>
            </Grid.Column>
            <Grid.Column>
              <Segment>
                <Checkbox
                  toggle
                  onChange={(e, d) => {
                    this.setState({
                      advancedView: d.checked
                    });
                  }}
                  label="Advanced View"
                />
              </Segment>
            </Grid.Column>
            <Grid.Column>
              <Segment>
                <Button
                  onClick={() => this.setState({ showUploadModal: true })}
                >
                  <Icon name="upload" />
                  Upload
                </Button>
                {/* </Segment>
                  <Segment> */}
                <Button
                  color="green"
                  disabled={content.length === 0}
                  onClick={e => {
                    if (whichObject == "table") {
                      this.fetchSQL(
                        JSON.stringify({
                          type: whichObject,
                          objects: content
                        })
                      );
                    } else {
                      this.fetchJava({
                        type: whichObject,
                        objects: content
                      });
                    }
                    // this.setState({ showViewGenerator: true })
                  }}
                >
                  <Icon name="cogs" /> Generate
                </Button>
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
              </Segment>
            </Grid.Column>
          </Grid.Row>
        </Grid>
        <Divider />
        <Grid>
          <Grid.Row columns={3}>
            {content.map((item, idx) => (
              <ObjectCreator
                item={item}
                key={idx}
                advancedView={advancedView}
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
