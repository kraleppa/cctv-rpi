import {React, useEffect, useState} from 'react';
import {Grid, Typography, IconButton} from '@material-ui/core';
import PhotoIcon from '@material-ui/icons/Photo';
import PhotosDialog from './PhotosDialog';
import FaceIcon from '@material-ui/icons/Face';
import PhotoCameraIcon from '@material-ui/icons/PhotoCamera';
import NotInterestedIcon from '@material-ui/icons/NotInterested';


// eslint-disable-next-line react/prop-types
const VideoElement = ({ip, onDelete}) => {
  const [faceDetection, setFaceDetection] = useState(false);
  const [dialog, setDialog] = useState(false);

  
  useEffect(() => {
    const fetchData = () => {
      fetch(`http://${ip}:5000/state`)
        .then(data => data.json())
        .then(json => setFaceDetection(json.face_detection));
    };
    const pollInterval = setInterval(() => fetchData(), 500);
    return () => {clearInterval(pollInterval); console.log(pollInterval);};
  }, []);


  const handleChange = () => {
    fetch(`http://${ip}:5000/detection/face`, {
      method: 'POST'
    });
  };

  const handleTakePhoto = () => {
    fetch(`http://${ip}:5000/images/save`, {
      method: 'POST',
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
            {
              faceDetection ? (
                <FaceIcon fontSize="large" color="primary" />
              ) : (
                <FaceIcon fontSize="large"/>
              )
            }
            
          </IconButton>
          <IconButton onClick={handleTakePhoto}>
            <PhotoCameraIcon fontSize="large" />
          </IconButton>
          <IconButton onClick={() => setDialog(true)}>
            <PhotoIcon fontSize="large"/>
          </IconButton>

          <IconButton onClick={() => onDelete(ip)}>
            <NotInterestedIcon fontSize="large"/>
          </IconButton>
        </Grid>


      </Grid>

      <PhotosDialog handleClose={() => setDialog(false)} ip={ip} open={dialog}/>
    </Grid>

  );
};

export default VideoElement;