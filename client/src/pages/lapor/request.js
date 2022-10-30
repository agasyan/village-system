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
import { getUserData } from "../../lib/auth"
import { Router } from 'next/router';

const Page = () => {
  const [documentTypeList, setDocumentTypeList] = useState([]);
  const [docTitle, setDocTitle] = useState("")
  const [description, setDescription] = useState("")
  // const fetchData = () => {
  //   axios
  //     .get('https://desa.agasyan.my.id/api/laporan-status/all')
  //     .then((response) => {
  //       const { data } = response;
  //       console.log(data)
  //       if (response.status === 200) {
  //         //check the api call is success by stats code 200,201 ...etc
  //         setDocumentTypeList(data.map(({ id, name }) => ({ label: id, value: name })))
  //       } else {
  //         //error handle section
  //       }
  //     })
  //     .catch((error) => console.log(error));

  // };
  const submitRequest = (event) => {
    axios
      .post('https://desa.agasyan.my.id/api/laporan', {
        title: docTitle,
        deskripsi: description,
        laporan_status_id: 1,
        user_id: getUserData().id
      })
      .then((response) => {
        alert("Berhasil membuat laporan")
        setDocTitle("")
        setDescription("")
        Router.push("/")
      })
      .catch((error) => console.log(error));
    event.preventDefault();
  }

  console.log(getUserData())

  return (
    <>
      <Head>
        <title>
        Pengajuan Laporan Kemalingan
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
                Pengajuan Laporan Kemalingan
              </Typography>
            </Box>
            <TextField
              fullWidth
              label="Laporan Terkait"
              margin="normal"
              name="title"
              onChange={(event) => { setDocTitle(event.target.value) }}
              variant="outlined"
            />
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
                Ajukan Laporan
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

