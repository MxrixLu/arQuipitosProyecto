import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  CircularProgress,
  Alert,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import config from '../config';

const MRIAnalysis = () => {
  const [mris, setMris] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedMRI, setSelectedMRI] = useState(null);
  const [diagnosis, setDiagnosis] = useState(null);
  const [loadingDiagnosis, setLoadingDiagnosis] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [patientId, setPatientId] = useState('');
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchMRIs();
  }, []);

  const fetchMRIs = async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/mris`);
      if (!response.ok) {
        throw new Error('Error al cargar los MRIs');
      }
      const data = await response.json();
      console.log('MRIs data:', data);
      setMris(data.mris);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchDiagnosis = async (mriId) => {
    try {
      setLoadingDiagnosis(true);
      console.log('Fetching diagnosis for MRI:', mriId);
      const response = await fetch(`${config.API_BASE_URL}/mri/${mriId}/diagnosis`);
      console.log('Diagnosis response status:', response.status);
      
      if (!response.ok) {
        throw new Error('Error al cargar el diagnóstico');
      }
      
      const diagnosisData = await response.json();
      console.log('Diagnosis data:', diagnosisData);
      
      if (diagnosisData && diagnosisData.diagnosis_text) {
        setDiagnosis(diagnosisData);
      } else {
        console.log('No diagnosis text found in response');
        setDiagnosis(null);
      }
    } catch (err) {
      console.error('Error fetching diagnosis:', err);
      setDiagnosis(null);
    } finally {
      setLoadingDiagnosis(false);
    }
  };

  const handleAnalyze = async (mriId) => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/mri/${mriId}/analyze`, {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Error al analizar el MRI');
      }
      await fetchMRIs();
      if (selectedMRI === mriId) {
        await fetchDiagnosis(mriId);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleMRIClick = async (mri) => {
    console.log('MRI clicked:', mri);
    setSelectedMRI(mri._id);
    await fetchDiagnosis(mri._id);
  };

  const handleCloseDialog = () => {
    setSelectedMRI(null);
    setDiagnosis(null);
  };

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile || !patientId) {
      setError('Por favor selecciona un archivo e ingresa un ID de paciente');
      return;
    }

    try {
      setUploading(true);
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('patient_id', patientId);

      const response = await fetch(`${config.API_BASE_URL}/mri/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Error al subir el MRI');
      }

      await fetchMRIs();
      setUploadDialogOpen(false);
      setSelectedFile(null);
      setPatientId('');
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Typography variant="h4" component="h1">
          Análisis de Imágenes MRI
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={() => setUploadDialogOpen(true)}
        >
          Subir Nuevo MRI
        </Button>
      </Box>
      
      <Grid container spacing={3}>
        {mris.map((mri) => (
          <Grid item xs={12} md={6} key={mri._id}>
            <Card 
              elevation={3}
              onClick={() => handleMRIClick(mri)}
              sx={{ 
                cursor: 'pointer',
                '&:hover': {
                  boxShadow: 6,
                  transform: 'translateY(-2px)',
                  transition: 'all 0.3s ease-in-out'
                }
              }}
            >
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  MRI ID: {mri._id}
                </Typography>
                <Typography color="textSecondary" gutterBottom>
                  Fecha de carga: {new Date(mri.upload_date).toLocaleString()}
                </Typography>
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  Paciente ID: {mri.patient_id || 'No especificado'}
                </Typography>
                
                <Box mt={2}>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleAnalyze(mri._id);
                    }}
                    sx={{ mr: 2 }}
                  >
                    Analizar MRI
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog 
        open={Boolean(selectedMRI)} 
        onClose={handleCloseDialog}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Detalles del Análisis MRI
        </DialogTitle>
        <DialogContent>
          {loadingDiagnosis ? (
            <Box display="flex" justifyContent="center" p={3}>
              <CircularProgress />
            </Box>
          ) : diagnosis ? (
            <Box mt={2}>
              <Typography variant="h6" gutterBottom>
                Diagnóstico:
              </Typography>
              <Paper elevation={1} sx={{ p: 2, bgcolor: '#f5f5f5' }}>
                <Typography variant="body1">
                  {diagnosis.diagnosis_text}
                </Typography>
              </Paper>
              <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
                Fecha del análisis: {new Date(diagnosis.analysis_date).toLocaleString()}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Analizado por: {diagnosis.analyzed_by}
              </Typography>
            </Box>
          ) : (
            <Typography variant="body1" color="textSecondary">
              No hay diagnóstico disponible para este MRI
            </Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cerrar</Button>
        </DialogActions>
      </Dialog>

      <Dialog
        open={uploadDialogOpen}
        onClose={() => setUploadDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          Subir Nuevo MRI
        </DialogTitle>
        <DialogContent>
          <Box mt={2}>
            <input
              accept="image/*"
              type="file"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
              id="mri-file-input"
            />
            <label htmlFor="mri-file-input">
              <Button
                variant="outlined"
                component="span"
                fullWidth
                sx={{ mb: 2 }}
              >
                Seleccionar Archivo MRI
              </Button>
            </label>
            {selectedFile && (
              <Typography variant="body2" sx={{ mb: 2 }}>
                Archivo seleccionado: {selectedFile.name}
              </Typography>
            )}
            <TextField
              fullWidth
              label="ID del Paciente"
              value={patientId}
              onChange={(e) => setPatientId(e.target.value)}
              margin="normal"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUploadDialogOpen(false)}>Cancelar</Button>
          <Button
            onClick={handleUpload}
            variant="contained"
            color="primary"
            disabled={uploading || !selectedFile || !patientId}
          >
            {uploading ? <CircularProgress size={24} /> : 'Subir MRI'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default MRIAnalysis; 