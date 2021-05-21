/* eslint-disable no-unused-vars */
import { Box, Button, Grid, TextField } from '@material-ui/core';
import React, { useState } from 'react';
import VideoElement from './VideoElement';

const VideosList = () => {
  // eslint-disable-next-line no-unused-vars
  const [videos, setVideos] = useState([]);
  const [text, setText] = useState('');

  const handleAdd = () => {
    setVideos(prev => [...prev, text]);
    setText('');
  };

  const handleClear = () => {
    setVideos([]);
    setText('');
  };

  const handleChange = (event) => {
    setText(event.target.value);
  };

  const handleDelete = (ip) => {
    setVideos(videos.filter(video => video !== ip));
  };
  
  
  return (
    <Box my={1}>
      <Grid container direction="column" spacing={5}>
        <Grid item container alignItems="center" direction="column" spacing={2}>
          <Grid item>
            <TextField id="outlined-basic" label="Adres IP" 
              variant="outlined" value={text} onChange={handleChange}/>
          </Grid>
          <Grid item>
            <Button variant="contained" color="primary" size="large" onClick={handleAdd}>Dodaj kamerę</Button>
          </Grid>
          <Grid item>
            <Button variant="contained" color="secondary" size="large" onClick={handleClear}>Wyczyść</Button>
          </Grid>


        </Grid>
        <Grid item container spacing={2} justify="center">
          {videos.map((video, i) => <VideoElement key={i} ip={video} onDelete={handleDelete} />)}
        </Grid>
      </Grid>
    </Box>


  );
};

export default VideosList;