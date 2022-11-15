import {
  Box,
  Button,Typography,Menu,
  MenuItem, MenuList, Popover
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import Router from 'next/router';
import { useRef, useState, useEffect } from 'react';

const DocumentMenu = (props) => {
  const { anchorEl, onClose, open, ...other } = props;

  return (
    <Menu
      anchorEl={anchorEl}
      elevation={0}
      anchorOrigin={{ vertical: "top", horizontal: "right" }}
      transformOrigin={{ vertical: "top", horizontal: "right" }}
      onClose={onClose}
      open={open}
      PaperProps={{
        sx: { width: '300px' }
      }}
      {...other}
    >
      <MenuList
        disablePadding
        sx={{
          '& > *': {
            '&:first-of-type': {
              borderTopColor: 'divider',
              borderTopStyle: 'solid',
              borderTopWidth: '1px'
            },
            padding: '12px 16px'
          }
        }}
      >
        <MenuItem onClick={() => Router.push('/document/request')}>
          Pengajuan Dokumen KK
        </MenuItem>
      </MenuList>
      <MenuList
        disablePadding
        sx={{
          '& > *': {
            '&:first-of-type': {
              borderTopColor: 'divider',
              borderTopStyle: 'solid',
              borderTopWidth: '1px'
            },
            padding: '12px 16px'
          }
        }}
      >
        <MenuItem onClick={() => Router.push('/document/ktp')}>
          Pengajuan Dokumen KTP
        </MenuItem>
      </MenuList>
    </Menu>
  );
};


export const DocumentListToolbar = (props) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
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
          List Dokumen
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
            onClick={handleClick}
            disableElevation
            id="demo-customized-button"
            aria-controls={open ? 'demo-customized-menu' : undefined}
            aria-haspopup="true"
            aria-expanded={open ? 'true' : undefined}
          >
            Buat Dokumen
          </Button>
          <DocumentMenu
            anchorEl={anchorEl}
            open={open}
            onClose={handleClose}
          />
        </Box>
      </Box>

    </Box>
  )
};
