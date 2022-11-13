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
import Router from 'next/router';

const Page = () => {
  const [documentTypeList, setDocumentTypeList] = useState([]);
  const [docTitle, setDocTitle] = useState("")
  const [description, setDescription] = useState("")
  const [gambar, setGambar] = useState("")
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
      .post('https://desa.agasyan.my.id/api/pengumuman', {
        title: docTitle,
        isi: description,
        gambar: gambar,
        user_id: getUserData().id
      })
      .then(() => {
        alert("Berhasil membuat pengumuman")
        setDocTitle("")
        setDescription("")
        setGambar("")
        Router.push("/")
      })
      .catch((error) => console.log(error));
    event.preventDefault();
  }


  return (
    <>
      <Head>
        <title>
        Membuat Pengumuman
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
                Membuat Pengumuman
              </Typography>
            </Box>
            <TextField
              fullWidth
              label="Judul Pengumuman"
              margin="normal"
              name="title"
              onChange={(event) => { setDocTitle(event.target.value) }}
              variant="outlined"
            />
            <TextField
              fullWidth
              label="Link Gambar"
              margin="normal"
              name="gambar"
              onChange={(event) => { setGambar(event.target.value) }}
              variant="outlined"
            />
            <TextField
              fullWidth
              label="Isi"
              margin="normal"
              name="deskripsi"
              multiline
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
                Buat
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

