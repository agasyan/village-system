import Head from 'next/head';
import { DashboardLayout } from '../../components/dashboard-layout';
import { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Container,
  TextField,
  Typography,
  Select,
  MenuItem,
  InputLabel,
  FormControl
} from '@mui/material';
import axios from 'axios';

const Page = () => {
  const [documentTypeList, setDocumentTypeList] = useState([]);
  const [docType, setDocType] = useState(0)
  const [docTitle, setDocTitle] = useState("")
  const [description, setDescription] = useState("")
  const fetchData = () => {
    axios
      .get('https://desa.agasyan.my.id/api/doc-type/all')
      .then((response) => {
        const { data } = response;
        console.log(data)
        if (response.status === 200) {
          //check the api call is success by stats code 200,201 ...etc
          setDocumentTypeList(data.map(({ id, name }) => ({ label: id, value: name })))
        } else {
          //error handle section 
        }
      })
      .catch((error) => console.log(error));
  };
  const submitRequest = (event) => {
    // todo doc user id
    axios
      .post('https://desa.agasyan.my.id/api/doc', {
        judul: docTitle,
        deskripsi: description,
        doc_status_id: 1,
        doc_type_id: docType,
        doc_user_id: 0
      })
      .then((response) => {
        console.log(response)
      })
      .catch((error) => console.log(error));
    event.preventDefault();
  }
  useEffect(() => {
    fetchData();
  }, [])
  return (
    <>
      <Head>
        <title>
          Request Dokumen
        </title>
      </Head>
      <Box
        component="main"
        sx={{
          alignItems: 'center',
          display: 'flex',
          flexGrow: 1,
          minHeight: '100%'
        }}
      >
        <Container maxWidth="sm">
          <form onSubmit={submitRequest}>
            <Box sx={{ my: 3 }}>
              <Typography
                color="textPrimary"
                variant="h4"
              >
                Request Dokumen
              </Typography>
            </Box>
            <FormControl fullWidth>
              <InputLabel id="demo-simple-select-label">Tipe Dokumen</InputLabel>
              <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={docType}
                onChange={(event) => {
                  setDocType(event.target.value);
                  const selectedDocumentType = documentTypeList.find(it => it.label === event.target.value);
                  setDocTitle(selectedDocumentType.value)
                }}
              >
                {documentTypeList.map((item) => (

                  <MenuItem key={item.label} value={item.label}>{item.value}</MenuItem>
                ))}

              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="Deskripsi"
              margin="normal"
              name="deskripsi"
              onChange={(event) => { setDescription(event.target.value) }}
              variant="outlined"
            />
            <Box sx={{ py: 2 }}>
              <Button
                color="primary"
                fullWidth
                size="large"
                type="submit"
                variant="contained"
              >
                Request Dokumen
              </Button>
            </Box>
          </form>
        </Container>
      </Box>
    </>
  );
};

Page.getLayout = (page) => (
  <DashboardLayout>
    {page}
  </DashboardLayout>
);

export default Page;

