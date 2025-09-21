
// components/ApplicationDetails.js
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  Button,
  Tabs,
  Tab,
  Paper,
  LinearProgress,
  Alert,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  ArrowBack,
  CheckCircle,
  Warning,
  TrendingUp,
  People,
  Business,
  Assessment,
} from '@mui/icons-material';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { apiCall } from '../utils/api';

const ApplicationDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [application, setApplication] = useState(null);
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState(0);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchApplicationDetails();
  }, [id]);

  const fetchApplicationDetails = async () => {
    try {
      const [appData, evalData] = await Promise.all([
        apiCall(`/api/applications/${id}`),
        apiCall(`/api/evaluations/${id}`).catch(() => null) // Evaluation might not exist yet
      ]);

      setApplication(appData);
      setEvaluation(evalData);
    } catch (error) {
      setError('Failed to load application details');
      console.error('Error fetching application details:', error);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 8) return '#4caf50';
    if (score >= 6) return '#ff9800';
    return '#f44336';
  };

  const getRecommendationColor = (recommendation) => {
    switch (recommendation) {
      case 'INVEST': return 'success';
      case 'REVIEW': return 'warning';
      case 'PASS': return 'error';
      default: return 'default';
    }
  };

  const scoreData = evaluation ? [
    { name: 'Founder Fit', score: evaluation.founder_market_fit_score },
    { name: 'Market Opportunity', score: evaluation.market_opportunity_score },
    { name: 'Business Model', score: evaluation.business_model_score },
    { name: 'Traction', score: evaluation.traction_score }
  ] : [];

  const riskData = evaluation ? [
    { name: 'Low Risk', value: evaluation.risk_level === 'LOW' ? 100 : 0, color: '#4caf50' },
    { name: 'Medium Risk', value: evaluation.risk_level === 'MEDIUM' ? 100 : 0, color: '#ff9800' },
    { name: 'High Risk', value: evaluation.risk_level === 'HIGH' ? 100 : 0, color: '#f44336' }
  ].filter(item => item.value > 0) : [];

  if (loading) {
    return (
      <Box sx={{ width: '100%', mt: 4 }}>
        <LinearProgress />
        <Typography sx={{ mt: 2, textAlign: 'center' }}>
          Loading application details...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mt: 4 }}>
        {error}
      </Alert>
    );
  }

  const TabPanel = ({ children, value, index }) => (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <Button
          startIcon={<ArrowBack />}
          onClick={() => navigate('/')}
          sx={{ mr: 2 }}
        >
          Back to Dashboard
        </Button>
        <Typography variant="h4" component="h1">
          {application?.company_name}
        </Typography>
      </Box>

      {/* Header Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Application Overview
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography color="text.secondary">Founders</Typography>
                  <Typography variant="body1">
                    {application?.founder_names.join(', ')}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography color="text.secondary">Funding Stage</Typography>
                  <Chip label={application?.funding_stage} variant="outlined" />
                </Grid>
                <Grid item xs={6}>
                  <Typography color="text.secondary">Team Size</Typography>
                  <Typography variant="body1">
                    {application?.team_size || 'Not specified'}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography color="text.secondary">Status</Typography>
                  <Chip
                    label={application?.status}
                    color={application?.status === 'evaluated' ? 'success' : 'warning'}
                  />
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              {evaluation ? (
                <>
                  <Typography variant="h6" gutterBottom>
                    Overall Score
                  </Typography>
                  <Typography
                    variant="h2"
                    sx={{ color: getScoreColor(evaluation.overall_score), fontWeight: 'bold' }}
                  >
                    {evaluation.overall_score.toFixed(1)}
                  </Typography>
                  <Chip
                    label={evaluation.recommendation}
                    color={getRecommendationColor(evaluation.recommendation)}
                    sx={{ mt: 1 }}
                  />
                </>
              ) : (
                <>
                  <Typography variant="h6" gutterBottom color="text.secondary">
                    Evaluation Pending
                  </Typography>
                  <LinearProgress sx={{ mt: 2 }} />
                </>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Detailed Tabs */}
      <Card>
        <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
          <Tab label="Business Details" />
          <Tab label="AI Analysis" disabled={!evaluation} />
          <Tab label="Scoring Breakdown" disabled={!evaluation} />
          <Tab label="Risk Assessment" disabled={!evaluation} />
        </Tabs>

        <TabPanel value={activeTab} index={0}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Business Description
              </Typography>
              <Typography variant="body1" sx={{ mb: 3 }}>
                {application?.business_description}
              </Typography>
            </Grid>

            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                Financial Information
              </Typography>
              <List>
                <ListItem disablePadding>
                  <ListItemText
                    primary="Funding Amount Sought"
                    secondary={application?.funding_amount ? `$${application.funding_amount.toLocaleString()}` : 'Not specified'}
                  />
                </ListItem>
                <ListItem disablePadding>
                  <ListItemText
                    primary="Current Revenue"
                    secondary={application?.revenue ? `$${application.revenue.toLocaleString()}` : 'Not specified'}
                  />
                </ListItem>
                <ListItem disablePadding>
                  <ListItemText
                    primary="Market Size"
                    secondary={application?.market_size || 'Not specified'}
                  />
                </ListItem>
              </List>
            </Grid>

            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                Resources
              </Typography>
              <List>
                {application?.pitch_deck_url && (
                  <ListItem disablePadding>
                    <ListItemText
                      primary="Pitch Deck"
                      secondary={
                        <Button size="small" href={application.pitch_deck_url} target="_blank">
                          View Deck
                        </Button>
                      }
                    />
                  </ListItem>
                )}
                {application?.pitch_video_url && (
                  <ListItem disablePadding>
                    <ListItemText
                      primary="Pitch Video"
                      secondary={
                        <Button size="small" href={application.pitch_video_url} target="_blank">
                          Watch Video
                        </Button>
                      }
                    />
                  </ListItem>
                )}
              </List>
            </Grid>
          </Grid>
        </TabPanel>

        <TabPanel value={activeTab} index={1}>
          {evaluation && (
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom color="success.main">
                  Key Insights
                </Typography>
                <List>
                  {evaluation.key_insights.map((insight, index) => (
                    <ListItem key={index} disablePadding>
                      <ListItemIcon>
                        <CheckCircle color="success" />
                      </ListItemIcon>
                      <ListItemText primary={insight} />
                    </ListItem>
                  ))}
                </List>
              </Grid>

              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom color="success.main">
                  Strengths
                </Typography>
                <List>
                  {evaluation.strengths.map((strength, index) => (
                    <ListItem key={index} disablePadding>
                      <ListItemIcon>
                        <TrendingUp color="success" />
                      </ListItemIcon>
                      <ListItemText primary={strength} />
                    </ListItem>
                  ))}
                </List>
              </Grid>

              <Grid item xs={12}>
                <Divider sx={{ my: 2 }} />
                <Typography variant="h6" gutterBottom color="warning.main">
                  Red Flags & Areas of Concern
                </Typography>
                <List>
                  {evaluation.red_flags.map((flag, index) => (
                    <ListItem key={index} disablePadding>
                      <ListItemIcon>
                        <Warning color="warning" />
                      </ListItemIcon>
                      <ListItemText primary={flag} />
                    </ListItem>
                  ))}
                </List>
              </Grid>
            </Grid>
          )}
        </TabPanel>

        <TabPanel value={activeTab} index={2}>
          {evaluation && (
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  Score Breakdown
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={scoreData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
                    <YAxis domain={[0, 10]} />
                    <Tooltip />
                    <Bar dataKey="score" fill="#1976d2" />
                  </BarChart>
                </ResponsiveContainer>
              </Grid>

              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  Individual Scores
                </Typography>
                <List>
                  <ListItem>
                    <ListItemText
                      primary="Founder-Market Fit"
                      secondary={`${evaluation.founder_market_fit_score}/10`}
                    />
                    <Box sx={{ width: 100, mr: 1 }}>
                      <LinearProgress
                        variant="determinate"
                        value={evaluation.founder_market_fit_score * 10}
                        sx={{ height: 8, borderRadius: 4 }}
                      />
                    </Box>
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Market Opportunity"
                      secondary={`${evaluation.market_opportunity_score}/10`}
                    />
                    <Box sx={{ width: 100, mr: 1 }}>
                      <LinearProgress
                        variant="determinate"
                        value={evaluation.market_opportunity_score * 10}
                        sx={{ height: 8, borderRadius: 4 }}
                      />
                    </Box>
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Business Model"
                      secondary={`${evaluation.business_model_score}/10`}
                    />
                    <Box sx={{ width: 100, mr: 1 }}>
                      <LinearProgress
                        variant="determinate"
                        value={evaluation.business_model_score * 10}
                        sx={{ height: 8, borderRadius: 4 }}
                      />
                    </Box>
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Traction"
                      secondary={`${evaluation.traction_score}/10`}
                    />
                    <Box sx={{ width: 100, mr: 1 }}>
                      <LinearProgress
                        variant="determinate"
                        value={evaluation.traction_score * 10}
                        sx={{ height: 8, borderRadius: 4 }}
                      />
                    </Box>
                  </ListItem>
                </List>
              </Grid>
            </Grid>
          )}
        </TabPanel>

        <TabPanel value={activeTab} index={3}>
          {evaluation && (
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  Risk Level Assessment
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={riskData}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name }) => name}
                    >
                      {riskData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
                <Typography sx={{ textAlign: 'center', mt: 2, fontWeight: 'bold' }}>
                  Risk Level: {evaluation.risk_level}
                </Typography>
              </Grid>

              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  Risk Mitigation Recommendations
                </Typography>
                <Alert severity="info" sx={{ mb: 2 }}>
                  AI-generated recommendations for addressing identified risks
                </Alert>
                <List>
                  {evaluation.red_flags.map((flag, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <Warning />
                      </ListItemIcon>
                      <ListItemText
                        primary={flag}
                        secondary="Consider deeper due diligence in this area"
                      />
                    </ListItem>
                  ))}
                </List>
              </Grid>
            </Grid>
          )}
        </TabPanel>
      </Card>
    </Box>
  );
};

export default ApplicationDetails;
