var jsdom = require('jsdom'),
    assert = require('assert'),
    testTimeline = require('../assets/timeline');

describe('HtmlRenderer', function(){
    var HtmlRenderer = require('../../src/app/renderer/HtmlRenderer');
    it('should init correctly', function () {
        var $el = $('<div></div>'),
            img = new Image();
        var html = new HtmlRenderer($el, testTimeline, img);
        assert.equal(html.canvas.length, 1);
    });
    it('should render frames', function () {
        var $el = $('<div></div>'),
            img = new Image();
        var html = new HtmlRenderer($el, testTimeline, img);
        html.renderFrame(0);
        assert.equal(html.canvas.html(), '<div style="position: absolute; width: 10px; height: 10px; background-image: url(); background-position: -0px -0px;"></div>');
        html.renderFrame(1);
        assert.equal(html.canvas.html(), '<div style="position: absolute; width: 10px; height: 10px; background-image: url(); background-position: -0px -0px;"></div><div style="position: absolute; width: 10px; height: 10px; background-image: url(); background-position: -0px -0px;"></div>');
    });
})
