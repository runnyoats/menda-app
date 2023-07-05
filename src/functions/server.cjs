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
		res.download('./students_submissions_data.xlsx');
	});
});

// ...other imports
const path = require('path');
const multer = require('multer'); // for handling multipart/form-data, which is used for file upload
const storage = multer.diskStorage({
	destination: function (req, file, cb) {
		cb(null, 'src/functions/tmp/');
	},
	filename: function (req, file, cb) {
		cb(null, file.originalname);
	}
});

const upload = multer({ storage: storage });

app.post('/import', upload.single('file'), (req, res) => {
	// Run import.py script on the uploaded file
	const filePath = req.file.path;
	// Quote the file path to handle spaces
	exec(`python3 ./src/functions/import.py "${filePath}"`, (error, stdout, stderr) => {
		if (error) {
			console.log(`error: ${error.message}`);
			return;
		}
		if (stderr) {
			console.log(`stderr: ${stderr}`);
			return;
		}
		console.log(`stdout: ${stdout}`);
	});

	res.send('Data imported successfully');
});

app.post('/sync', express.json(), (req, res) => {
	const { username, password, year } = req.body;

	exec(
		`python3 ./src/webscraper/sepkm_scraper.py "${username}" "${password}" "${year}"`,
		(error, stdout, stderr) => {
			if (error) {
				console.log(`error: ${error.message}`);
				res.status(500).send({ error: error.message });
				return;
			}
			if (stderr) {
				console.log(`stderr: ${stderr}`);
				res.status(500).send({ error: stderr });
				return;
			}

			res.status(200).send({ message: stdout });
		}
	);
});

app.listen(port, () => {
	console.log(`Server running at http://localhost:${port}/`);
});
