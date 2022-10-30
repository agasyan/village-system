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
  FormControl,
} from '@mui/material';
import axios from 'axios';
import { getUserData } from "../../lib/auth"
import { Router } from 'next/router';

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
    event.preventDefault();
    axios
      .post('https://desa.agasyan.my.id/api/doc', {
        judul: docTitle,
        deskripsi: description,
        doc_status_id: 1,
        doc_type_id: docType,
        doc_user_id: getUserData().id,
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
  useEffect(() => {
    fetchData();
  }, [])
  return (
    <>
      <Head>
        <title>
          Request Dokumen KK
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
                Request Dokumen KK
              </Typography>
            </Box>
            <FormControl fullWidth>
              <InputLabel id="demo-simple-select-label">Tipe Pengajuan KK</InputLabel>
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
              label="Dokumen Pendukung (link google drive)"
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
                Request Dokumen KK
              </Button>
            </Box>
          </form>
          <Typography>
          DOKUMEN PENDUKUNG PENGAJUAN KK <br></br><br></br>
1. Pembuatan KK Baru<br></br>
    1. Surat pengantar dari ketua RT yang sudah ditandatangani ketua RW<br></br>
    2. Surat keterangan pindah (khusus untuk pendatang)<br></br>
    3. Fotokopi buku nikah atau akta perkawinan<br></br><br></br>
2. Penambahan Anggota Keluarga karena Menumpang<br></br>
    1. Kartu keluarga anggota keluarga menumpang<br></br>
    2. Kartu keluarga dari keluarga yg ditumpangi<br></br>
    3. Surat keterangan pindah datang (WNI)<br></br>
    4. Surat keterangan datang dari luar negeri (WNI dari luar negeri)<br></br>
    5. Fotokopi buku nikah<br></br>
    6. Surat keterangan penduduk<br></br><br></br>
3. Penambahan anggota keluarga karena kelahiran<br></br>
    1. Kartu keluarga sebelum<br></br>
    2. Surat nikah orang tua<br></br>
    3. KTP orang tua<br></br>
    4. Surat Keterangan lahir<br></br><br></br><br></br>

tiap dokumen silakan di upload pada satu folder google drive dan submit link pada form
          </Typography>
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

