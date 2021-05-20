/* eslint-disable react/prop-types */
import {React, useEffect, useState} from 'react';

import Dialog from '@material-ui/core/Dialog';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';
import Typography from '@material-ui/core/Typography';
import ListItemText from '@material-ui/core/ListItemText';
import ListItem from '@material-ui/core/ListItem';
import List from '@material-ui/core/List';
import Box from '@material-ui/core/Box';
import Divider from '@material-ui/core/Divider';
import { DialogContent } from '@material-ui/core';

const PhotosDialog = ({ip, handleClose, open}) => {
  const [photos, setPhotos] = useState([]);
  const [photo, setPhoto] = useState('');

  useEffect(() => {
    fetch(`http://${ip}:5000/images/names`)
      .then(data => data.json())
      .then(json => setPhotos(json.images));
  }, [photo]);

  const renderPhoto = (name) => {
    return (
      <>
        <ListItem button onClick={() => setPhoto(name)}>
          <ListItemText primary={name} />
        </ListItem>
        <Divider />
      </>
    );
  };

  console.log(photo);

  return (
    <Dialog fullScreen open={open} onClose={handleClose}>
      <AppBar style={{position: 'relative'}}>
        <Toolbar>
          <IconButton edge="start" color="inherit" onClick={handleClose} aria-label="close">
            <CloseIcon />
          </IconButton>
          <Typography variant="h6">
            Zdjęcia {ip} 
          </Typography>
        </Toolbar>
      </AppBar>
      <List>
        <Divider />
        {photos.sort().map(photo => renderPhoto(photo))}
      </List>
      <DialogContent>
        <Box display="flex" justifyContent="center">
          {photo && <img src={`http://${ip}:5000/images/id/${photo}`}/>}
        </Box>


      </DialogContent>

    </Dialog>
  );
};

export default PhotosDialog;