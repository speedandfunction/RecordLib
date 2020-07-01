import React, { useState } from "react";
import { connect } from "react-redux";
import Paper from "@material-ui/core/Paper";
import Container from "@material-ui/core/Container";
import List from "@material-ui/core/List";
import Button from "@material-ui/core/Button";
import { makeStyles } from "@material-ui/core/styles";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import Typography from "@material-ui/core/Typography";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import CircularProgress from "@material-ui/core/CircularProgress";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import { uploadRecords } from "frontend/src/actions/localFiles";
import SourceRecordRow from "frontend/src/components/SourceRecordRow";
/*
 *   Step in the Petition analysis and generation process for uploading files for processing.
 *
 *   This component is for uploading summary and docket files, sending them to the server,
 *   and receiving the resulting CRecord.
 */

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    marginTop: "2rem",
  },
  paper: {
    padding: "2rem",
    marginBottom: "2rem",
  },
  title: {
    margin: theme.spacing(4, 0, 2),
  },
}));

// Helper component to show a list of the files selected.
function FileList(props) {
  const { selectedFiles } = props;
  if (selectedFiles.length > 0) {
    return (
      <List>
        {selectedFiles.map((f, index) => {
          return (
            <ListItem key={index}>
              <ListItemText primary={f.name} />
            </ListItem>
          );
        })}
      </List>
    );
  } else {
    return <div> No files selected yet </div>;
  }
}

/**
 *
 *   Component to select files and dispatch api call to upload them.
 * */
function SourceRecords(props) {
  const classes = useStyles();

  const [selectedFiles, setSelectedFiles] = useState([]);

  const { uploadRecords, isUploadPending, sourceRecords } = props;

  const onChangeHandler = (event) => {
    setSelectedFiles([...event.target.files]);
  };

  const onClickHandler = (e) => {
    e.preventDefault();
    setSelectedFiles([]);
    uploadRecords(selectedFiles);
  };

  return (
    <Container className={classes.root}>
      <Paper className={classes.paper}>
        <Typography variant="h3">Source Records</Typography>
        <Typography variant="body1">
          Documents, such as docket sheets, that are already used to compile the
          current criminal record.
        </Typography>
        {isUploadPending ? (
          <CircularProgress />
        ) : sourceRecords.allIds.length === 0 ? (
          <Typography>No records processed yet.</Typography>
        ) : (
          <Table aria-label="processed source records">
            <TableHead>
              <TableRow>
                <TableCell>Caption</TableCell>
                <TableCell>Docket Number</TableCell>
                <TableCell>Court</TableCell>
                <TableCell>URL</TableCell>
                <TableCell>Record Type</TableCell>
                <TableCell>Fetch Status</TableCell>
                <TableCell>Parse Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {sourceRecords.allIds.map((srID) => {
                return (
                  <SourceRecordRow
                    key={srID}
                    record={sourceRecords.allSourceRecords[srID]}
                  ></SourceRecordRow>
                );
              })}
            </TableBody>
          </Table>
        )}
      </Paper>
      <Paper className={classes.paper}>
        <Typography variant="h3"> Upload files </Typography>
        <p> Select the summary and docket files you wish to analyze.</p>
        <FileList selectedFiles={selectedFiles} />
        <form encType="multipart/form-data" onSubmit={onClickHandler}>
          <input multiple type="file" name="file" onChange={onChangeHandler} />
          <Button type="submit"> Upload </Button>
        </form>
      </Paper>
    </Container>
  );
}

// TODO see if there is another way to notify the user that their upload succeeded.  Right now the condition below is always true.
//function mapStateToProps(state) {
//    return {crecordFetched: state.crecord? true: false};
//};

function mapDispatchToProps(dispatch) {
  return {
    uploadRecords: (files) => dispatch(uploadRecords(files)),
  };
}

function mapStateToProps(state) {
  return {
    sourceRecords: state.sourceRecords,
    isUploadPending: state.ujsSearchResults.uploadUJSDocs.pending,
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(SourceRecords);
