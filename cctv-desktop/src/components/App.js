import { Box } from '@material-ui/core';
import React from 'react';
import VideosList from './VideosList';

const App = () => {
  return (
    <Box style={{overflowX: 'hidden', overflowY: 'hidden'}}>
      <VideosList />
    </Box>
  );
};

export default App;
