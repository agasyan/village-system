import Head from 'next/head';
import { Box, Container, Typography, Button } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { DashboardLayout } from '../components/dashboard-layout';
import { PengumumanList } from '../components/pengumuman/pengumuman-list';
import Router from 'next/router';

const Page = () => (
  <>
    <Head>
      <title>
        Dashboard | Material Kit
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
        <Box width="100%" display="flex" flexDirection="row" justifyContent="space-between">
        <Typography variant="h3">Pengumuman</Typography>
        <Button
          startIcon={(<AddIcon />)}
          sx={{ mr: 1 }}
          onClick={() => Router.push('/pengumuman/create')}
        >
          Buat Pengumuman
        </Button>
        </Box>

        <Box sx={{ mt: 3 }}>
          <PengumumanList />
        </Box>
      </Container>
    </Box>
  </>
);

Page.getLayout = (page) => (
  <DashboardLayout>
    {page}
  </DashboardLayout>
);

export default Page;
