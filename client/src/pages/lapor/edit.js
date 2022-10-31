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
import Router, { useRouter } from 'next/router';

const Page = () => {
  const [documentTypeList, setDocumentTypeList] = useState([]);
  const [docTitle, setDocTitle] = useState("")
  const [docType, setDocType] = useState("")
  const [description, setDescription] = useState("")
  const [address, setAddress] = useState("")
  const [laporanData, setLaporanData] = useState({})
  const router = useRouter()
  const { id } = router.query;

  const fetchLaporan = () => {
    axios
      .get(`https://desa.agasyan.my.id/api/laporan/${id}`)
      .then((response) => {
        const { data } = response;
        if (response.status === 200) {
          setLaporanData(data)
          setDocTitle(data.title)
          setDescription(data.deskripsi)
          setDocType(data.laporan_status.laporan_status_id)
          setAddress(data.alamat)
        } else {
          //error handle section
        }
      })
      .catch((error) => console.log(error));

  };

  const fetchLaporanStatus = () => {
    axios
      .get('https://desa.agasyan.my.id/api/laporan-status/all')
      .then((response) => {
        const { data } = response;
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
    axios
      .post('https://desa.agasyan.my.id/api/laporan', {
        title: docTitle,
        deskripsi: description,
        laporan_status_id: docType,
        alamat: address,
        user_id: getUserData().id
      })
      .then(() => {
        alert("Berhasil mengubab laporan")
        setDocTitle("")
        setDescription("")
        setAddress("")
        setDocType("")
        Router.push("/lapor/list")
      })
      .catch((error) => console.log(error));
    event.preventDefault();
  }

  useEffect(() => {
    fetchLaporan();
    fetchLaporanStatus();
  }, [])

  console.log(documentTypeList)
  console.log(docType)
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
                Ubah Status Laporan Kemalingan
              </Typography>
            </Box>
            <InputLabel style={{ marginTop: "8px"}}>Judul Laporan Terkait</InputLabel>
            <TextField
              fullWidth
              hiddenLabel
              margin="normal"
              name="title"
              value={laporanData.title}
              disabled
              onChange={(event) => { setDocTitle(event.target.value) }}
              variant="outlined"
            />
            <InputLabel style={{ marginTop: "8px"}}>Alamat</InputLabel>
            <TextField
              hiddenLabel
              fullWidth
              margin="normal"
              disabled
              value={laporanData.alamat}
              name="address"
              onChange={(event) => { setAddress(event.target.value) }}
              variant="outlined"
            />
            <InputLabel style={{ marginTop: "8px"}}>Deskripsi</InputLabel>
            <TextField
              hiddenLabel
              fullWidth
              margin="normal"
              name="deskripsi"
              value={laporanData.deskripsi}
              disabled
              multiline
              onChange={(event) => { setDescription(event.target.value) }}
              variant="outlined"
            />
            <InputLabel style={{ marginTop: "8px", marginBottom: "8px"}}>Status Laporan</InputLabel>
            <FormControl fullWidth>
              <Select
                hiddenLabel
                value={docType}
                onChange={(event) => {
                  setDocType(event.target.value);
                }}
              >
                {documentTypeList.map((item) => (

                  <MenuItem key={item.value} value={item.label}>{item.value}</MenuItem>
                ))}

              </Select>
            </FormControl>
            <Box sx={{ py: 2 }}>
              <Button
                color="primary"
                fullWidth
                size="large"
                type="submit"
                variant="contained"
              >
                Ubah Laporan
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

