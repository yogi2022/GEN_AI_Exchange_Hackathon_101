# Create the React frontend implementation
react_frontend = '''
// App.js - Main React Application
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import Dashboard from './components/Dashboard';
import ApplicationForm from './components/ApplicationForm';
import ApplicationDetails from './components/ApplicationDetails';
import Navbar from './components/Navbar';
import { AuthProvider, useAuth } from './contexts/AuthContext';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    h1: {
      fontWeight: 700,
    },
    h2: {
      fontWeight: 600,
    },
  },
});

function AppContent() {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <div>Please log in to access the AI Startup Analyst Platform</div>
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <Box component="main" sx={{ flexGrow: 1, p: 3, mt: 8 }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/apply" element={<ApplicationForm />} />
          <Route path="/applications/:id" element={<ApplicationDetails />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Box>
    </Box>
  );
}

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <AppContent />
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
'''

with open("App.js", "w") as f:
    f.write(react_frontend)

print("✅ Created App.js - Main React Application")

# Create Dashboard component
dashboard_component = '''
// components/Dashboard.js
import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
} from '@mui/material';
import {
  TrendingUp,
  Assessment,
  People,
  CheckCircle,
  Schedule,
  Warning,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { apiCall } from '../utils/api';

const Dashboard = () => {
  const [metrics, setMetrics] = useState({});
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedApp, setSelectedApp] = useState(null);
  const [agentStatus, setAgentStatus] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardData();
    fetchApplications();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const data = await apiCall('/api/dashboard/metrics');
      setMetrics(data);
    } catch (error) {
      console.error('Error fetching dashboard metrics:', error);
    }
  };

  const fetchApplications = async () => {
    try {
      const data = await apiCall('/api/applications');
      setApplications(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching applications:', error);
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'submitted': return 'info';
      case 'processing': return 'warning';
      case 'evaluated': return 'success';
      case 'error': return 'error';
      default: return 'default';
    }
  };

  const MetricCard = ({ title, value, icon, color = 'primary' }) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          {icon}
          <Typography variant="h6" sx={{ ml: 1 }}>
            {title}
          </Typography>
        </Box>
        <Typography variant="h3" color={color}>
          {value}
        </Typography>
      </CardContent>
    </Card>
  );

  const handleViewApplication = (app) => {
    navigate(`/applications/${app.id}`);
  };

  const handleViewAgentStatus = async (appId) => {
    try {
      const status = await apiCall(`/api/agent-status/${appId}`);
      setAgentStatus(status);
      setSelectedApp(appId);
    } catch (error) {
      console.error('Error fetching agent status:', error);
    }
  };

  if (loading) {
    return (
      <Box sx={{ width: '100%', mt: 4 }}>
        <LinearProgress />
        <Typography sx={{ mt: 2, textAlign: 'center' }}>
          Loading dashboard...
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          AI Startup Analyst Dashboard
        </Typography>
        <Button
          variant="contained"
          size="large"
          onClick={() => navigate('/apply')}
          sx={{ borderRadius: '25px' }}
        >
          Submit New Application
        </Button>
      </Box>

      {/* Metrics Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Total Applications"
            value={metrics.total_applications || 0}
            icon={<Assessment color="primary" />}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Evaluated"
            value={metrics.evaluated_applications || 0}
            icon={<CheckCircle color="success" />}
            color="success"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Processing"
            value={metrics.pending_evaluation || 0}
            icon={<Schedule color="warning" />}
            color="warning"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Accuracy Rate"
            value={metrics.accuracy_rate || "N/A"}
            icon={<TrendingUp color="info" />}
            color="info"
          />
        </Grid>
      </Grid>

      {/* Applications Table */}
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            Recent Applications
          </Typography>
          <TableContainer component={Paper} sx={{ mt: 2 }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Company Name</TableCell>
                  <TableCell>Founders</TableCell>
                  <TableCell>Funding Stage</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Submitted</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {applications.slice(0, 10).map((app) => (
                  <TableRow key={app.id}>
                    <TableCell>
                      <Typography variant="subtitle2">
                        {app.company_name}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      {app.founder_names.join(', ')}
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={app.funding_stage}
                        size="small"
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={app.status}
                        color={getStatusColor(app.status)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      {new Date(app.created_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      <Button
                        size="small"
                        onClick={() => handleViewApplication(app)}
                        sx={{ mr: 1 }}
                      >
                        View
                      </Button>
                      {app.status === 'processing' && (
                        <Button
                          size="small"
                          variant="outlined"
                          onClick={() => handleViewAgentStatus(app.id)}
                        >
                          Status
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Agent Status Dialog */}
      <Dialog
        open={Boolean(selectedApp)}
        onClose={() => setSelectedApp(null)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>AI Agent Processing Status</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            {Object.entries(agentStatus).map(([agent, status]) => (
              <Grid item xs={12} md={6} key={agent}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      {agent.replace('_', ' ').toUpperCase()} Agent
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Chip
                        label={status.status}
                        color={status.status === 'completed' ? 'success' : 'warning'}
                        size="small"
                      />
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={status.progress}
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      {status.progress}% complete
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </DialogContent>
      </Dialog>
    </Box>
  );
};

export default Dashboard;
'''

with open("Dashboard.js", "w") as f:
    f.write(dashboard_component)

print("✅ Created Dashboard.js - Main dashboard component")

# Create Application Form component
application_form = '''
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
'''

with open("ApplicationForm.js", "w") as f:
    f.write(application_form)

print("✅ Created ApplicationForm.js - Application submission form")

# Create package.json for React app
package_json = '''{
  "name": "ai-startup-analyst-frontend",
  "version": "1.0.0",
  "description": "React frontend for AI-powered startup evaluation platform",
  "main": "src/index.js",
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "dependencies": {
    "@mui/material": "^5.14.18",
    "@mui/icons-material": "^5.14.18",
    "@emotion/react": "^11.11.1",
    "@emotion/styled": "^11.11.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.18.0",
    "react-scripts": "5.0.1",
    "axios": "^1.6.2",
    "recharts": "^2.8.0",
    "date-fns": "^2.30.0",
    "@mui/x-charts": "^6.18.1",
    "@mui/x-data-grid": "^6.18.1"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "devDependencies": {
    "@types/react": "^18.2.38",
    "@types/react-dom": "^18.2.17"
  }
}'''

with open("package.json", "w") as f:
    f.write(package_json)

print("✅ Created package.json for React application")

print("\n🎯 Frontend Implementation Summary:")
print("  - Complete React application with Material-UI")
print("  - Multi-step application form with validation")
print("  - Real-time dashboard with metrics")
print("  - Agent status monitoring")
print("  - Responsive design for all screen sizes")
print("  - Modern UI/UX with professional styling")