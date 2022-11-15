import Head from 'next/head';
import { Box, Container, MenuItem, MenuList, Popover, Typography} from '@mui/material';
import { DashboardLayout } from '../../components/dashboard-layout';
import axios from 'axios';
import Router from 'next/router';
import { useEffect, useState } from 'react';
import { DocumentList } from '../../components/document/document-list';
import { DocumentListToolbar } from '../../components/document/document-list-toolbar';

const Page = () => {
  const [docList, setDocList] = useState([]);
  const fetchData = () => {
    axios
      .get('https://desa.agasyan.my.id/api/doc/all')
      .then((response) => {
        const { data } = response;
        console.log(data)
        if (response.status === 200) {
          //check the api call is success by stats code 200,201 ...etc
          setDocList(data)
        } else {
          //error handle section
        }
      })
      .catch((error) => console.log(error));
  };

  useEffect(() => {
    fetchData();
  }, []);
  return (
    <>
      <Head>
        <title>
          Customers | Material Kit
        </title>
      </Head>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          py: 8
        }}
      >
        <Container maxWidth={false}>
          <DocumentListToolbar />
          <Box sx={{ mt: 3 }}>
            <DocumentList documents={docList} />
          </Box>
        </Container>
      </Box>
    </>
  );
}

Page.getLayout = (page) => (
  <DashboardLayout>
    {page}
  </DashboardLayout>
);

export default Page;
