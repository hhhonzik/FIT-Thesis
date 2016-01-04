var jsdom = require('jsdom'),
    assert = require('assert'),
    testTimeline = require('./assets/timeline');

describe('Controller', function(){
    // create some jsdom magic to allow jQuery to work
    var doc = jsdom.jsdom(),
        window = doc.parentWindow,
        $ = global.jQuery = require('jquery')(window);
    global.Image = doc.parentWindow.Image;
    global.document = doc;
    global.$ = global.jQuery;

    var Controller = require('../src/app/controller');

    it('test default values', function () {
        var isDone = false;
        var c = new Controller({
            timelineData: testTimeline,
            src: './assets/packed.png',
            $el: $('<div></div>')
        });

        assert.equal(c.playing, false);
        assert.equal(c.loop, false);
        assert.equal(c.speed, 500);
        assert.equal(c.data.frames.length, 2);

    });

    it('test onLoad event and correct renderer', function (done) {
        var isDone = false;
        var c = new Controller({
            timelineData: testTimeline,
            src: './assets/packed.png',
            html5: false,
            onLoad: function () {
                if (isDone) {
                    return;
                }
                isDone = true;
                done();
            },
            $el: $('<div></div>')
        });
        assert.equal(c.renderer.canvas[0]._localName, 'div');
    });
})
