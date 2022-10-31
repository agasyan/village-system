import {
  Box,
  Button,Typography
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { Upload as UploadIcon } from '../../icons/upload';
import { Download as DownloadIcon } from '../../icons/download';
import Router from 'next/router';

export const ReportListToolbar = (props) => (
  <Box {...props}>
    <Box
      sx={{
        alignItems: 'center',
        display: 'flex',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        m: -1
      }}
    >
      <Typography
        sx={{ m: 1 }}
        variant="h4"
      >
        List Laporan
      </Typography>
      <Box sx={{ m: 1 }}>
        {/* <Button
          startIcon={(<UploadIcon fontSize="small" />)}
          sx={{ mr: 1 }}
        >
          Import
        </Button>
        <Button
          startIcon={(<DownloadIcon fontSize="small" />)}
          sx={{ mr: 1 }}
        >
          Export
        </Button> */}
        <Button
          startIcon={(<AddIcon />)}
          sx={{ mr: 1 }}
          onClick={() => Router.push('/lapor/request')}
        >
          Buat Laporan
        </Button>
      </Box>
    </Box>
  </Box>
);
