
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
