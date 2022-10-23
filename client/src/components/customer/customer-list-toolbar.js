import {
  Box,
  Button,Typography
} from '@mui/material';
import { Upload as UploadIcon } from '../../icons/upload';
import { Download as DownloadIcon } from '../../icons/download';

export const CustomerListToolbar = (props) => (
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
        List Issue
      </Typography>
      <Box sx={{ m: 1 }}>
        <Button
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
        </Button>
      </Box>
    </Box>
  </Box>
);
