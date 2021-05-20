import {React, useState} from 'react';
import PropTypes from 'prop-types';
import {Grid, Typography, IconButton} from '@material-ui/core';
import PhotoIcon from '@material-ui/icons/Photo';
import PhotosDialog from './PhotosDialog';
import FaceIcon from '@material-ui/icons/Face';


const VideoElement = ({ip}) => {
  // eslint-disable-next-line no-unused-vars
  const [faceDetection, setFaceDetection] = useState(false);
  const [dialog, setDialog] = useState(false);


  const handleChange = () => {
    fetch(`http://${ip}:5000/detection/face`, {
      method: 'POST'
    });
  };

  return (
    <Grid item >
      <img src={`http://${ip}:5000/`}/>
      <Grid container alignItems="center" justify="space-between">
        <Grid item>
          <Typography variant="h4" display="inline" >{ip}</Typography>
        </Grid>

        <Grid item>
          <IconButton onClick={handleChange}>
            <FaceIcon fontSize="large"/>
          </IconButton>
          <IconButton onClick={() => setDialog(true)}>
            <PhotoIcon fontSize="large"/>
          </IconButton>
        </Grid>


      </Grid>

      <PhotosDialog handleClose={() => setDialog(false)} ip={ip} open={dialog}/>
    </Grid>

  );
};

VideoElement.propTypes = {
  ip: PropTypes.string
};
  

export default VideoElement;