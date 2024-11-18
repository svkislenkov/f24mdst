const express = require('express');
const app = express();
const repl = require('repl');
const { PythonShell } = require('python-shell');

// Important: These middleware declarations should come before routes
app.use(express.json());
app.use(express.static('public'));

// Store leaderboard in memory
let leaderboard = [];

// Get leaderboard
app.get('/api/leaderboard', (req, res) => {
    res.json(leaderboard);
});

// Submit new opinion
app.post('/api/opinions', (req, res) => {
    const { name, opinion } = req.body;
    
    console.log('Received opinion:', opinion);

    let options = {
        mode: 'text',
        pythonPath: 'python',
        scriptPath: './',
        args: [opinion],
        encoding: 'utf8'
    };

    PythonShell.run('trainer.py', options)
        .then(results => {
            console.log('Python script output:', results);
            
            try {
                // Get the last line which contains our prediction
                const lastLine = results[results.length - 1];
                const ratio = parseFloat(lastLine.split(':')[1]);
                
                const newEntry = { 
                    id: Date.now().toString(),
                    name, 
                    opinion, 
                    upvoteRatio: ratio
                };
                
                leaderboard.push(newEntry);
                leaderboard.sort((a, b) => b.upvoteRatio - a.upvoteRatio);
                if (leaderboard.length > 10) {
                    leaderboard.pop();
                }
                
                res.json({ upvoteRatio: ratio, leaderboard });
                
            } catch (error) {
                console.error('Error parsing Python output:', error);
                res.status(500).json({ 
                    error: 'Failed to parse prediction',
                    details: error.message 
                });
            }
        })
        .catch(err => {
            console.error('Python script error:', err);
            res.status(500).json({ 
                error: 'Failed to run Python script',
                details: err.message 
            });
        });
});

// Delete endpoint
app.delete('/api/entries/:id', (req, res) => {
    const { id } = req.params;
    console.log('Attempting to delete entry with ID:', id); // Add this for debugging
    
    const initialLength = leaderboard.length;
    leaderboard = leaderboard.filter(entry => entry.id !== id);
    
    if (leaderboard.length === initialLength) {
        console.log('Entry not found'); // Add this for debugging
        res.status(404).json({ error: 'Entry not found' });
    } else {
        console.log('Entry deleted successfully'); // Add this for debugging
        res.json({ message: 'Entry deleted successfully', leaderboard });
    }
});

const PORT = 3000;
const server = app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    
    // Start REPL
    const replServer = repl.start({
        prompt: 'server > ',
        useColors: true
    });

    // Add commands to REPL context
    replServer.context.leaderboard = leaderboard;
    replServer.context.listEntries = () => {
        console.table(leaderboard);
    };
    replServer.context.deleteEntry = (id) => {
        const initialLength = leaderboard.length;
        leaderboard = leaderboard.filter(entry => entry.id !== id);
        if (leaderboard.length === initialLength) {
            console.log('Entry not found');
        } else {
            console.log('Entry deleted successfully');
        }
    };
});