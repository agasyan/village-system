import { Card, Checkbox, Table, TableBody, TableCell, TableHead, TablePagination, TableRow, Typography } from "@mui/material";
import { Box } from "@mui/system";
import { useState } from "react";
import PropTypes from 'prop-types';
import PerfectScrollbar from 'react-perfect-scrollbar';
import Router from "next/router";

export const DocumentList = ({ documents, ...rest }) => {
    const [selectedDocIds, setSelectedDocIds] = useState([]);
    const [limit, setLimit] = useState(10);
    const [page, setPage] = useState(0);

    const handleSelectAll = (event) => {
        let newSelectedDocIds;

        if (event.target.checked) {
            newSelectedDocIds = documents.map((doc) => doc.id);
        } else {
            newSelectedDocIds = [];
        }

        setSelectedDocIds(newSelectedDocIds);
    };

    const handleSelectOne = (event, id) => {
        const selectedIndex = selectedDocIds.indexOf(id);
        let newSelectedDocIds = [];

        if (selectedIndex === -1) {
            newSelectedDocIds = newSelectedDocIds.concat(selectedDocIds, id);
        } else if (selectedIndex === 0) {
            newSelectedDocIds = newSelectedDocIds.concat(selectedDocIds.slice(1));
        } else if (selectedIndex === selectedDocIds.length - 1) {
            newSelectedDocIds = newSelectedDocIds.concat(selectedDocIds.slice(0, -1));
        } else if (selectedIndex > 0) {
            newSelectedDocIds = newSelectedDocIds.concat(
                selectedDocIds.slice(0, selectedIndex),
                selectedDocIds.slice(selectedIndex + 1)
            );
        }

        setSelectedDocIds(newSelectedDocIds);
    };

    const handleLimitChange = (event) => {
        setLimit(event.target.value);
    };

    const handlePageChange = (event, newPage) => {
        setPage(newPage);
    };

    return (
        <Card {...rest}>
            <PerfectScrollbar>
                <Box sx={{ minWidth: 1050 }}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell padding="checkbox">
                                    <Checkbox
                                        checked={selectedDocIds.length === documents.length}
                                        color="primary"
                                        indeterminate={
                                            selectedDocIds.length > 0
                                            && selectedDocIds.length < documents.length
                                        }
                                        onChange={handleSelectAll}
                                    />
                                </TableCell>
                                <TableCell>
                                    Judul
                                </TableCell>
                                <TableCell>
                                    Deskripsi
                                </TableCell>
                                <TableCell>
                                    Status
                                </TableCell>
                                <TableCell>
                                    Tipe
                                </TableCell>
                                <TableCell>
                                    Pengaju
                                </TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {documents.slice(page * limit, (page * limit) + limit).map((document) => (
                                <TableRow
                                    hover
                                    key={document.id}
                                    onClick={() => Router.push(`/document/edit?id=${document.id}`)}
                                    selected={selectedDocIds.indexOf(document.id) !== -1}
                                >
                                    <TableCell padding="checkbox">
                                        <Checkbox
                                            checked={selectedDocIds.indexOf(document.id) !== -1}
                                            onChange={(event) => handleSelectOne(event, document.id)}
                                            value="true"
                                        />
                                    </TableCell>
                                    <TableCell>
                                        {document.judul}
                                    </TableCell>
                                    <TableCell>
                                        <Box
                                            sx={{
                                                alignItems: 'center',
                                                display: 'flex'
                                            }}
                                        >
                                            <Typography
                                                color="textPrimary"
                                                variant="body1"
                                            >
                                                {document.deskripsi}
                                            </Typography>
                                        </Box>
                                    </TableCell>
                                    <TableCell>
                                        {document.doc_status.name}
                                    </TableCell>
                                    <TableCell>
                                        {document.doc_type.name}
                                    </TableCell>
                                    <TableCell>
                                        {document.created_by_user.full_name}
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </Box>
            </PerfectScrollbar>
            <TablePagination
                component="div"
                count={documents.length}
                onPageChange={handlePageChange}
                onRowsPerPageChange={handleLimitChange}
                page={page}
                rowsPerPage={limit}
                rowsPerPageOptions={[5, 10, 25]}
            />
        </Card>
    );
};

DocumentList.propTypes = {
    documents: PropTypes.array.isRequired
};
