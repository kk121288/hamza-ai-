// Import necessary modules
const express = require('express');
const path = require('path');

// Create Express app
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.static('public'));

// API Routes
app.get('/api/health', (req, res) => {
    res.json({
        status: 'healthy',
        uptime: process.uptime(),
        timestamp: new Date().toISOString(),
        accuracy: 95
    });
});

app.post('/api/detect_ai', (req, res) => {
    const { text } = req.body;
    
    // Your AI detection logic here
    const aiProbability = Math.random() * 0.3 + 0.6; // Demo value
    
    res.json({
        ai_probability: aiProbability,
        human_probability: 1 - aiProbability,
        confidence: 0.85,
        language: 'ar',
        word_count: text.split(/\s+/).length,
        analysis: {
            patterns_found: {
                ai_patterns: Math.floor(Math.random() * 5),
                human_patterns: Math.floor(Math.random() * 3)
            }
        }
    });
});

// Serve HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});