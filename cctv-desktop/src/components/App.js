import { Box } from '@material-ui/core';
import React from 'react';
import Layout from './Layout';
import VideosList from './VideosList';

const App = () => {
  return (
    <Box style={{overflowX: 'hidden', overflowY: 'hidden'}}>
      <Layout>
        <VideosList />
      </Layout>
    </Box>
  );
};

export default App;
