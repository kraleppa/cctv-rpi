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
import NotInterestedIcon from '@material-ui/icons/NotInterested';

const PhotosDialog = ({ip, handleClose, open}) => {
  const [photos, setPhotos] = useState([]);
  const [photo, setPhoto] = useState('');

  useEffect(() => {
    fetch(`http://${ip}:5000/images/names`)
      .then(data => data.json())
      .then(json => setPhotos(json.images));
  }, [open]);

  const handleDelete = (event, name) => {
    event.stopPropagation();
    event.cancelBubble = true;
    setPhoto('');
    setPhotos(photos.filter(photo => photo !== name));
    fetch(`http://${ip}:5000/images/id/${name}`, {
      method: 'DELETE'
    }).catch(error => console.warn(error));
  };

  const handlePick = (event, name) => {
    event.stopPropagation();
    event.cancelBubble = true;
    setPhoto(name);
  };

  const renderPhoto = (name) => {
    return (
      <Box key={name}>         
        <ListItem button onClick={(event) => handlePick(event, name)}>
          <ListItemText primary={name} />
          <IconButton onClick={(event) => handleDelete(event, name)}>
            <NotInterestedIcon fontSize="large" color="secondary"/>
          </IconButton>
        </ListItem>
        <Divider />
      </Box>

    );
  };

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