import {React, useState} from 'react';
import PropTypes from 'prop-types';
import {Grid, Box, Typography, IconButton} from '@material-ui/core';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import PhotoIcon from '@material-ui/icons/Photo';


const VideoElement = ({ip}) => {
  // eslint-disable-next-line no-unused-vars
  const [faceDetection, setFaceDetection] = useState(false);


  const handleChange = () => {
    fetch(`http://${ip}:5000/detection/face`, {
      method: 'POST'
    });
  };

  return (
    <Grid item >
      <Box textAlign="center">
        <Typography variant="h4">{ip}</Typography>
      </Box>
      <img src={`http://${ip}:5000/`}/>
      <Box mt={3}>
        <Grid container justify="space-around">
          <Grid item>
            <FormControlLabel
              control={
                <Switch
                  checked={faceDetection}
                  onChange={handleChange}
                  name="checkedB"
                  color="primary"
                />
              }
              label="Wykrywanie twarzy"
            />
          </Grid>
          <Grid item>
            <IconButton>
              <PhotoIcon fontSize="large"/>
            </IconButton>
          </Grid>
        </Grid>

      </Box>
    </Grid>

  );
};

VideoElement.propTypes = {
  ip: PropTypes.string
};
  

export default VideoElement;