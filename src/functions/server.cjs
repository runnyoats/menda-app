const express = require('express');
const { exec } = require('child_process');
const cors = require('cors');
const app = express();
app.use(cors());
const port = 3000;

app.get('/export', (req, res) => {
	exec('python3 ./src/functions/export.py', (error, stdout, stderr) => {
		if (error) {
			console.log(`error: ${error.message}`);
			res.sendStatus(500);
			return;
		}
		if (stderr) {
			console.log(`stderr: ${stderr}`);
			res.sendStatus(500);
			return;
		}
		res.download('./students_data.xlsx');
	});
});

app.listen(port, () => {
	console.log(`Server running at http://localhost:${port}/`);
});
