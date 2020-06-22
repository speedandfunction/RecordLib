import React from "react";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import Link from "@material-ui/core/Link";
/**
 *
 * One row in a Table containing information about a single SourceRecord.
 *
 * @param {*} props
 */
function SourceRecordRow(props) {
  const { record, childKey } = props;
  return (
    <TableRow key={childKey}>
      <TableCell align="left">{record.caption}</TableCell>
      <TableCell align="left">{record.docket_num}</TableCell>
      <TableCell align="left">{record.court}</TableCell>
      <TableCell align="left">
        {record.url.length > 0 ? (
          <Link href={record.url}>Link</Link>
        ) : (
          record.url
        )}
      </TableCell>
      <TableCell align="left">{record.record_type}</TableCell>
      <TableCell align="left">{record.fetch_status}</TableCell>
      <TableCell align="left">{record.parse_status}</TableCell>
    </TableRow>
  );
}

export default SourceRecordRow;
