import React from 'react';
import { Box, Grid, Button, Container } from '@mui/material';

const Request = () => {
  return (
    <Container maxWidth="md">
      <Box mt={4}>
        {/* First row - 3 centered buttons */}
        <Grid container spacing={2} justifyContent="center">
          <Grid item>
            <Button variant="contained" color="primary">
              PSCRF Data
            </Button>
          </Grid>
          <Grid item>
            <Button variant="contained" color="primary">
              Unsigned Approved Contract
            </Button>
          </Grid>
          <Grid item>
            <Button variant="contained" color="primary">
              Signed Client Contract
            </Button>
          </Grid>
        </Grid>

        {/* Second row - 2 centered buttons */}
        <Box mt={4}>
          <Grid container spacing={2} justifyContent="center">
            <Grid item>
              <Button variant="outlined" color="secondary">
                One-Way
              </Button>
            </Grid>
            <Grid item>
              <Button variant="outlined" color="secondary">
                Bi-Directional
              </Button>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
};

export default Request;
