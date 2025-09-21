# Create additional React components and utilities
auth_context = '''
// contexts/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing auth token
    const token = localStorage.getItem('auth_token');
    if (token) {
      setIsAuthenticated(true);
      setUser({ role: 'analyst', name: 'Demo User' });
    }
    setLoading(false);
  }, []);

  const login = async (credentials) => {
    try {
      // Mock login - replace with real authentication
      if (credentials.email === 'demo@example.com' && credentials.password === 'demo') {
        const token = 'demo-token';
        localStorage.setItem('auth_token', token);
        setIsAuthenticated(true);
        setUser({ role: 'analyst', name: 'Demo User', email: credentials.email });
        return { success: true };
      }
      return { success: false, error: 'Invalid credentials' };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    setIsAuthenticated(false);
    setUser(null);
  };

  const value = {
    isAuthenticated,
    user,
    loading,
    login,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
'''

with open("AuthContext.js", "w") as f:
    f.write(auth_context)

# Create API utility
api_utils = '''
// utils/api.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const apiCall = async (endpoint, method = 'GET', data = null) => {
  const token = localStorage.getItem('auth_token');
  
  const config = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }

  if (data && method !== 'GET') {
    config.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};

export const uploadFile = async (endpoint, file) => {
  const token = localStorage.getItem('auth_token');
  const formData = new FormData();
  formData.append('file', file);

  const config = {
    method: 'POST',
    headers: {},
    body: formData
  };

  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
  } catch (error) {
    console.error('File upload failed:', error);
    throw error;
  }
};
'''

with open("api.js", "w") as f:
    f.write(api_utils)

# Create Application Details component
application_details = '''
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
'''

with open("ApplicationDetails.js", "w") as f:
    f.write(application_details)

# Create Navbar component
navbar_component = '''
// components/Navbar.js
import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  Menu,
  MenuItem,
} from '@mui/material';
import { AccountCircle, Dashboard, Add } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    handleClose();
  };

  return (
    <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
          🤖 AI Startup Analyst
        </Typography>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Button
            color="inherit"
            startIcon={<Dashboard />}
            onClick={() => navigate('/')}
            sx={{ textTransform: 'none' }}
          >
            Dashboard
          </Button>
          
          <Button
            color="inherit"
            startIcon={<Add />}
            onClick={() => navigate('/apply')}
            sx={{ textTransform: 'none' }}
          >
            New Application
          </Button>

          <IconButton
            size="large"
            aria-label="account of current user"
            aria-controls="menu-appbar"
            aria-haspopup="true"
            onClick={handleMenu}
            color="inherit"
          >
            <AccountCircle />
          </IconButton>
          <Menu
            id="menu-appbar"
            anchorEl={anchorEl}
            anchorOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            keepMounted
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            open={Boolean(anchorEl)}
            onClose={handleClose}
          >
            <MenuItem disabled>
              <Typography variant="body2" color="text.secondary">
                {user?.name || 'Demo User'}
              </Typography>
            </MenuItem>
            <MenuItem disabled>
              <Typography variant="body2" color="text.secondary">
                Role: {user?.role || 'Analyst'}
              </Typography>
            </MenuItem>
            <MenuItem onClick={handleLogout}>Logout</MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
'''

with open("Navbar.js", "w") as f:
    f.write(navbar_component)

# Create deployment scripts
docker_compose = '''version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}
      - GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS}
      - API_SECRET_KEY=${API_SECRET_KEY}
    volumes:
      - ./service-account.json:/app/service-account.json:ro
    depends_on:
      - postgres
      - redis

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - backend

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=startup_analyst
      - POSTGRES_USER=analyst
      - POSTGRES_PASSWORD=password123
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
'''

with open("docker-compose.yml", "w") as f:
    f.write(docker_compose)

# Create startup script
startup_script = '''#!/bin/bash

# AI Startup Analyst Platform - Quick Start Script

echo "🚀 Starting AI Startup Analyst Platform..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
mkdir -p frontend/src/components
mkdir -p frontend/src/contexts
mkdir -p frontend/src/utils

# Copy frontend files to proper structure
echo "📁 Setting up frontend structure..."
mv App.js frontend/src/
mv Dashboard.js frontend/src/components/
mv ApplicationForm.js frontend/src/components/
mv ApplicationDetails.js frontend/src/components/
mv Navbar.js frontend/src/components/
mv AuthContext.js frontend/src/contexts/
mv api.js frontend/src/utils/
mv package.json frontend/

# Create frontend Dockerfile
cat > frontend/Dockerfile << EOF
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
EOF

# Create frontend index.js
cat > frontend/src/index.js << EOF
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOF

# Create public/index.html
mkdir -p frontend/public
cat > frontend/public/index.html << EOF
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="AI-powered startup evaluation platform" />
    <title>AI Startup Analyst</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
EOF

# Set up environment variables
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp .env.example .env
    echo "⚠️  Please update the .env file with your actual API keys and credentials"
fi

# Start the application
echo "🐳 Starting Docker containers..."
docker-compose up --build -d

echo "✅ Application started successfully!"
echo ""
echo "🌐 Access the application at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""
echo "📊 Database connections:"
echo "   PostgreSQL: localhost:5432"
echo "   Redis: localhost:6379"
echo ""
echo "🔧 To stop the application, run: docker-compose down"
echo "📝 To view logs, run: docker-compose logs -f"
'''

with open("start.sh", "w") as f:
    f.write(startup_script)

# Make startup script executable
import os
os.chmod("start.sh", 0o755)

print("✅ Created additional React components:")
print("  - AuthContext.js - Authentication management")
print("  - api.js - API utility functions")
print("  - ApplicationDetails.js - Detailed application view")
print("  - Navbar.js - Navigation component")
print("  - docker-compose.yml - Multi-service orchestration")
print("  - start.sh - Quick start script")

print("\n🎯 Complete Full-Stack Implementation Ready!")
print("📦 Total files created:")
print("  - Backend: FastAPI with multi-agent system")
print("  - Frontend: React with Material-UI")
print("  - Database: PostgreSQL + Redis")
print("  - Deployment: Docker + Docker Compose")
print("  - Documentation: Comprehensive README")