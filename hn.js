var request = require('request');
var cheerio = require('cheerio');

var url = 'https://news.ycombinator.com/';
request(url, function(err, resp, body) {
    // if (error && response.statusCode == 200) {
    if (err) throw err;

    $ = cheerio.load(body);
    $('td.subtext a:nth-child(3)').each(function() {
        // comments = $(this).text().trim();//.match(/\d+/);
        comments = $(this).text().trim().replace(/[^0-9]/g, '');
        console.log(comments);
    });
})
