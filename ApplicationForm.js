
// components/ApplicationForm.js
import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Grid,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Chip,
  OutlinedInput,
  Paper,
  Stepper,
  Step,
  StepLabel,
  Alert,
  CircularProgress,
} from '@mui/material';
import { CloudUpload, Send } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { apiCall } from '../utils/api';

const ApplicationForm = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    company_name: '',
    founder_names: [''],
    email: '',
    business_description: '',
    funding_stage: '',
    funding_amount: '',
    team_size: '',
    revenue: '',
    market_size: '',
    pitch_deck_url: '',
    pitch_video_url: '',
  });

  const steps = ['Company Info', 'Founders & Team', 'Business Details', 'Submit'];

  const fundingStages = [
    'Pre-Seed',
    'Seed',
    'Series A',
    'Series B', 
    'Series C',
    'Growth',
    'Pre-IPO'
  ];

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleFounderChange = (index, value) => {
    const newFounders = [...formData.founder_names];
    newFounders[index] = value;
    setFormData(prev => ({
      ...prev,
      founder_names: newFounders
    }));
  };

  const addFounder = () => {
    setFormData(prev => ({
      ...prev,
      founder_names: [...prev.founder_names, '']
    }));
  };

  const removeFounder = (index) => {
    if (formData.founder_names.length > 1) {
      const newFounders = formData.founder_names.filter((_, i) => i !== index);
      setFormData(prev => ({
        ...prev,
        founder_names: newFounders
      }));
    }
  };

  const handleNext = () => {
    if (validateStep(activeStep)) {
      setActiveStep(prev => prev + 1);
    }
  };

  const handleBack = () => {
    setActiveStep(prev => prev - 1);
  };

  const validateStep = (step) => {
    switch (step) {
      case 0:
        return formData.company_name && formData.email;
      case 1:
        return formData.founder_names.every(name => name.trim() !== '');
      case 2:
        return formData.business_description && formData.funding_stage;
      default:
        return true;
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');

    try {
      const cleanedData = {
        ...formData,
        founder_names: formData.founder_names.filter(name => name.trim() !== ''),
        funding_amount: formData.funding_amount ? parseFloat(formData.funding_amount) : null,
        team_size: formData.team_size ? parseInt(formData.team_size) : null,
        revenue: formData.revenue ? parseFloat(formData.revenue) : null,
      };

      const response = await apiCall('/api/applications', 'POST', cleanedData);
      setSubmitSuccess(true);

      setTimeout(() => {
        navigate(`/applications/${response.id}`);
      }, 2000);
    } catch (error) {
      setError('Failed to submit application. Please try again.');
      console.error('Submission error:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Company Name"
                value={formData.company_name}
                onChange={(e) => handleInputChange('company_name', e.target.value)}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Contact Email"
                type="email"
                value={formData.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                required
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Pitch Deck URL (Optional)"
                value={formData.pitch_deck_url}
                onChange={(e) => handleInputChange('pitch_deck_url', e.target.value)}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Pitch Video URL (Optional)"
                value={formData.pitch_video_url}
                onChange={(e) => handleInputChange('pitch_video_url', e.target.value)}
              />
            </Grid>
          </Grid>
        );

      case 1:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Founder Information
              </Typography>
              {formData.founder_names.map((founder, index) => (
                <Box key={index} sx={{ display: 'flex', mb: 2, alignItems: 'center' }}>
                  <TextField
                    fullWidth
                    label={`Founder ${index + 1} Name`}
                    value={founder}
                    onChange={(e) => handleFounderChange(index, e.target.value)}
                    required
                    sx={{ mr: 1 }}
                  />
                  {formData.founder_names.length > 1 && (
                    <Button
                      onClick={() => removeFounder(index)}
                      color="error"
                      variant="outlined"
                      size="small"
                    >
                      Remove
                    </Button>
                  )}
                </Box>
              ))}
              <Button onClick={addFounder} variant="outlined" size="small">
                + Add Another Founder
              </Button>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Team Size"
                type="number"
                value={formData.team_size}
                onChange={(e) => handleInputChange('team_size', e.target.value)}
              />
            </Grid>
          </Grid>
        );

      case 2:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={4}
                label="Business Description"
                value={formData.business_description}
                onChange={(e) => handleInputChange('business_description', e.target.value)}
                required
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth required>
                <InputLabel>Funding Stage</InputLabel>
                <Select
                  value={formData.funding_stage}
                  onChange={(e) => handleInputChange('funding_stage', e.target.value)}
                >
                  {fundingStages.map(stage => (
                    <MenuItem key={stage} value={stage}>{stage}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Funding Amount Sought ($)"
                type="number"
                value={formData.funding_amount}
                onChange={(e) => handleInputChange('funding_amount', e.target.value)}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Current Revenue ($)"
                type="number"
                value={formData.revenue}
                onChange={(e) => handleInputChange('revenue', e.target.value)}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Market Size (Optional)"
                value={formData.market_size}
                onChange={(e) => handleInputChange('market_size', e.target.value)}
                placeholder="e.g., $10B TAM"
              />
            </Grid>
          </Grid>
        );

      case 3:
        return (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            {submitSuccess ? (
              <Alert severity="success" sx={{ mb: 3 }}>
                Application submitted successfully! Redirecting to application details...
              </Alert>
            ) : (
              <>
                <Typography variant="h6" gutterBottom>
                  Review Your Application
                </Typography>
                <Typography color="text.secondary" sx={{ mb: 3 }}>
                  Please review your information before submitting. Our AI agents will begin
                  analysis immediately upon submission.
                </Typography>

                <Paper sx={{ p: 3, mb: 3, textAlign: 'left' }}>
                  <Typography><strong>Company:</strong> {formData.company_name}</Typography>
                  <Typography><strong>Founders:</strong> {formData.founder_names.join(', ')}</Typography>
                  <Typography><strong>Funding Stage:</strong> {formData.funding_stage}</Typography>
                  <Typography><strong>Team Size:</strong> {formData.team_size || 'Not specified'}</Typography>
                </Paper>

                {error && (
                  <Alert severity="error" sx={{ mb: 3 }}>
                    {error}
                  </Alert>
                )}
              </>
            )}
          </Box>
        );

      default:
        return null;
    }
  };

  return (
    <Box sx={{ maxWidth: 900, mx: 'auto' }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
        Submit Startup Application
      </Typography>

      <Paper sx={{ p: 4 }}>
        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        <Card>
          <CardContent sx={{ p: 4 }}>
            {renderStepContent(activeStep)}
          </CardContent>
        </Card>

        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3 }}>
          <Button
            onClick={handleBack}
            disabled={activeStep === 0}
            variant="outlined"
          >
            Back
          </Button>

          {activeStep === steps.length - 1 ? (
            <Button
              onClick={handleSubmit}
              disabled={loading || submitSuccess}
              variant="contained"
              size="large"
              startIcon={loading ? <CircularProgress size={20} /> : <Send />}
            >
              {loading ? 'Submitting...' : 'Submit Application'}
            </Button>
          ) : (
            <Button
              onClick={handleNext}
              variant="contained"
              disabled={!validateStep(activeStep)}
            >
              Next
            </Button>
          )}
        </Box>
      </Paper>
    </Box>
  );
};

export default ApplicationForm;
