import React from 'react';
import PropTypes from 'prop-types';
import {Grid, Box, Typography, Button} from '@material-ui/core';

const VideoElement = ({ip}) => {
  const handleChange = () => {
    fetch(`http://${ip}:5000/detection/face`, {
      method: 'POST'
    });
  };

  return (
    <Grid item >
      <img src={`http://${ip}:5000/`}/>
      <Box textAlign="center">
        <Typography variant="h4">{ip}</Typography>
        <Box mt={3}>
          <Button variant="contained" onClick={handleChange}>
            Rozponawanie twarzy
          </Button>
          <Box style={{borderRadius: '50%'}}>
            
          </Box>
      
        </Box>

      </Box>

    </Grid>

  );
};

VideoElement.propTypes = {
  ip: PropTypes.string
};
  

export default VideoElement;