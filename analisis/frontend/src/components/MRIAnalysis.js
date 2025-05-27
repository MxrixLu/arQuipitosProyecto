import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Grid,
  Typography,
  CircularProgress,
  Alert,
} from '@mui/material';

const MRIAnalysis = () => {
  const [mris, setMris] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [patientId, setPatientId] = useState('');

  const fetchMRIs = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/mris');
      const data = await response.json();
      setMris(data.mris);
    } catch (err) {
      setError('Error fetching MRIs');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchMRIs();
  }, [fetchMRIs]);

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile || !patientId) {
      setError('Please select a file and enter a patient ID');
      return;
    }

    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('patient_id', patientId);

      const response = await fetch('http://localhost:8000/mri/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Upload failed');

      await fetchMRIs();
      setSelectedFile(null);
      setPatientId('');
    } catch (err) {
      setError('Error uploading MRI');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async (mriId) => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:8000/mri/${mriId}/analyze`, {
        method: 'POST',
      });

      if (!response.ok) throw new Error('Analysis failed');

      await fetchMRIs();
    } catch (err) {
      setError('Error analyzing MRI');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        MRI Analysis System
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Upload New MRI
          </Typography>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={4}>
              <input
                accept="image/*"
                type="file"
                onChange={handleFileSelect}
                style={{ display: 'none' }}
                id="mri-file-input"
              />
              <label htmlFor="mri-file-input">
                <Button variant="contained" component="span">
                  Select MRI File
                </Button>
              </label>
              {selectedFile && (
                <Typography variant="body2" sx={{ mt: 1 }}>
                  Selected: {selectedFile.name}
                </Typography>
              )}
            </Grid>
            <Grid item xs={12} sm={4}>
              <input
                type="text"
                placeholder="Patient ID"
                value={patientId}
                onChange={(e) => setPatientId(e.target.value)}
                style={{
                  padding: '8px',
                  width: '100%',
                  border: '1px solid #ccc',
                  borderRadius: '4px',
                }}
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <Button
                variant="contained"
                color="primary"
                onClick={handleUpload}
                disabled={loading || !selectedFile || !patientId}
              >
                Upload MRI
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Typography variant="h6" gutterBottom>
        MRI List
      </Typography>

      {loading ? (
        <Box display="flex" justifyContent="center" my={4}>
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={2}>
          {mris.map((mri) => (
            <Grid item xs={12} sm={6} md={4} key={mri._id}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    MRI ID: {mri._id}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Patient ID: {mri.patient_id}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Upload Date: {new Date(mri.upload_date).toLocaleString()}
                  </Typography>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={() => handleAnalyze(mri._id)}
                    sx={{ mt: 2 }}
                  >
                    Analyze MRI
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
};

export default MRIAnalysis; 