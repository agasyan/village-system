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
  const [docStatusList, setDocStatusList] = useState([]);
  const [docDetail, setDocDetail] = useState({});
  
  const [docTitle, setDocTitle] = useState("")
  const [docType, setDocType] = useState("")
  const [docStatus, setDocStatus] = useState(0)
  const [description, setDescription] = useState("")
  const router = useRouter()
  const { id } = router.query;

  const fetchDocDetail = () => {
    axios
      .get(`https://desa.agasyan.my.id/api/doc/${id}`)
      .then((response) => {
        const { data } = response;
        if (response.status === 200) {
          setDocDetail(data)
          setDocTitle(data.judul)
          setDescription(data.deskripsi)
          setDocStatus(data.doc_status.id)
          setDocType(data.doc_type.id)
        } else {
          //error handle section
        }
      })
      .catch((error) => console.log(error));

  };

  const fetchDocStatus = () => {
    axios
      .get('https://desa.agasyan.my.id/api/doc-status/all')
      .then((response) => {
        const { data } = response;
        if (response.status === 200) {
          //check the api call is success by stats code 200,201 ...etc
          setDocStatusList(data)
        } else {
          //error handle section
        }
      })
      .catch((error) => console.log(error));

  };

  const fetchDocType = () => {
    axios
      .get('https://desa.agasyan.my.id/api/doc-type/all')
      .then((response) => {
        const { data } = response;
        if (response.status === 200) {
          //check the api call is success by stats code 200,201 ...etc
          setDocumentTypeList(data)
        } else {
          //error handle section
        }
      })
      .catch((error) => console.log(error));

  };

  const submitRequest = (event) => {
    axios
      .put(`https://desa.agasyan.my.id/api/doc/${id}`, {
        judul: docTitle,
        deskripsi: description,
        doc_status_id: docStatus,
        doc_type_id: docType,
        user_id: getUserData().id
      })
      .then(() => {
        alert("Berhasil mengubah dokumen status")
        setDocTitle("")
        setDescription("")
        setAddress("")
        setDocType("")
        Router.push("/document/list")
      })
      .catch((error) => console.log(error));
    event.preventDefault();
  }

  useEffect(() => {
    fetchDocDetail();
    fetchDocStatus();
    fetchDocType();
  }, [])

  return (
    <>
      <Head>
        <title>
        Update Pengajuan Dokumen
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
                Update Pengajuan Dokumen
              </Typography>
            </Box>
            <InputLabel style={{ marginTop: "8px"}}>Judul Dokumen</InputLabel>
            <TextField
              fullWidth
              hiddenLabel
              margin="normal"
              name="judul"
              value={docDetail.judul}
              disabled
              onChange={(event) => { setDocTitle(event.target.value) }}
              variant="outlined"
            />
            <InputLabel style={{ marginTop: "8px"}}>File upload</InputLabel>
            <TextField
              hiddenLabel
              fullWidth
              margin="normal"
              disabled
              value={docDetail.deskripsi}
              name="deskripsi"
              onChange={(event) => { setDescription(event.target.value) }}
              variant="outlined"
            />
            <InputLabel style={{ marginTop: "8px", marginBottom: "8px"}}>Tipe Dokumen</InputLabel>
            <FormControl fullWidth>
              <Select
                hiddenLabel
                value={docType}
                onChange={(event) => {
                  setDocType(event.target.value);
                }}
              >
                {documentTypeList.map((item) => (

                  <MenuItem key={item.id} value={item.name}>{item.name}</MenuItem>
                ))}

              </Select>
            </FormControl>
            <InputLabel style={{ marginTop: "8px", marginBottom: "8px"}}>Status Dokumen</InputLabel>
            <FormControl fullWidth>
              <Select
                hiddenLabel
                value={docType}
                onChange={(event) => {
                  setDocStatus(event.target.value);
                }}
              >
                {docStatusList.map((item) => (

                  <MenuItem key={item.id} value={item.name}>{item.name}</MenuItem>
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
                Ubah Pengajuan Dokumen
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

