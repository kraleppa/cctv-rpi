import React from 'react';
import PropTypes from 'prop-types';
import { Grid } from '@material-ui/core';

const VideoElement = ({imgUrl}) => {
  return (
    <Grid item >
      <img src={imgUrl}/>
    </Grid>

  );
};

VideoElement.propTypes = {
  imgUrl: PropTypes.string
};
  

export default VideoElement;