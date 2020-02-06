import React from "react"
import TableRow from "@material-ui/core/TableRow"
import TableCell from "@material-ui/core/TableCell"
import Link from "@material-ui/core/Link"
/**
 * 
 * One row in a Table containing information about a single SourceRecord.
 * 
 * @param {*} props 
 */
function SourceRecordRow(props) {
    const {record, key} = props
    return(
        <TableRow key={key}>
            <TableCell align="left">{record.caption}</TableCell>
            <TableCell align="left">{record.docket_num}</TableCell>
            <TableCell align="left">{record.court}</TableCell>
            <TableCell align="left">
                {
                    record.url.length > 0 ?
                        <Link to={record.url}>Link</Link> :
                        record.url 
                }
            </TableCell>
            <TableCell align="left">{record.record_type}</TableCell>
            <TableCell align="left">{record.fetch_status}</TableCell>
        </TableRow>
    )
}


export default SourceRecordRow;


