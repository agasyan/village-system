import Head from 'next/head';
import { Box, Container, Typography } from '@mui/material';
import { DashboardLayout } from '../components/dashboard-layout';
import { PengumumanList } from '../components/pengumuman/pengumuman-list';
import { pengumuman } from '../__mocks__/pengumuman';

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
      
        <Typography variant="h3">Pengumuman</Typography>
        <Box sx={{ mt: 3 }}>
          <PengumumanList pengumumans={pengumuman} />
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
