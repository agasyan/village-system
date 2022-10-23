import Head from 'next/head';
import { Box, Container } from '@mui/material';
import { CustomerListResults } from '../../components/customer/customer-list-results';
import { CustomerListToolbar } from '../../components/customer/customer-list-toolbar';
import { DashboardLayout } from '../../components/dashboard-layout';
import { customers } from '../../__mocks__/customers';

const Page = () => {
  const [issueList, setIssueList] = useState(issues);
  const fetchData = () => {
    axios
      .get('https://desa.agasyan.my.id/api/issue/all')
      .then((response) => {
        const { data } = response;
        console.log(data)
        if (response.status === 200) {
          //check the api call is success by stats code 200,201 ...etc
          setIssueList(data)
        } else {
          //error handle section 
        }
      })
      .catch((error) => console.log(error));
  };
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
          <CustomerListToolbar />
          <Box sx={{ mt: 3 }}>
            <CustomerListResults issues={issueList} />
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
