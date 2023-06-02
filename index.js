const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

const fs = require('fs');

const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

json = JSON.parse(fs.readFileSync('./JSON/shares.json', 'utf8'));

app.get('/'|| '/all', (req, res) => {
    res.send(json)
});

app.listen(port, () => {
    console.log(`http://localhost:${port}`);
}
);