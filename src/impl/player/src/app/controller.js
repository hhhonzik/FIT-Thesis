module.exports = (function () {
    "use strict";
    var CanvasRenderer = require('./renderer/CanvasRenderer'),
        HtmlRenderer = require('./renderer/HtmlRenderer');
    function isCanvasSupported() {
        var elem = document.createElement('canvas');
        return !!(elem.getContext && elem.getContext('2d'));
    }
    // definition of Controller class
    function Controller(options) {
        var self = this;
        self.data = {};
        self.playing = false;
        self.loop = options.loop || false;
        options.html5 = (options.hasOwnProperty('html5')) ? options.html5 : true;
        self.currentFrame = null;
        self.speed = options.speed || 500;
        self.events = {
            'onLoad': [],
            'onFrame': [],
            'onPlay': [],
            'onStop': []
        };
        if (typeof options.onLoad === "function") {
            self.onEvent('onLoad', options.onLoad);
        }
        if (typeof options.onFrame === "function") {
            self.onEvent('onFrame', options.onFrame);
        }
        if (typeof options.onPlay === "function") {
            self.onEvent('onPlay', options.onPlay);
        }
        if (typeof options.onStop === "function") {
            self.onEvent('onStop', options.onStop);
        }
        function afterTimeline(data) {
            if (!data) {
                throw new Error('Timeline data not found');
            }
            self.data = data;
            self.image = new Image();
            self.image.onload = function () {
                // we have image & timeline data
                if (isCanvasSupported() && options.html5) {
                    self.renderer = new CanvasRenderer(options.$el, data, self.image);
                } else {
                    self.renderer = new HtmlRenderer(options.$el, data, self.image);
                }
                self.renderFrame(0);
                self.fireEvent('onLoad');
                if (options.autoplay) {
                    setTimeout(function () {
                        self.play();
                    }, 10);
                }
            };
            self.image.src = options.src;
        }
        if (options.timeline) {
            $.getJSON(options.timeline, function (timelineData) {
                // we have timeline data
                afterTimeline(timelineData);
            });
        } else {

            afterTimeline(options.timelineData);
        }
    }
    Controller.prototype.play = function () {
        if (!this.playing) {
            this.fireEvent('onPlay');
            this.playing = true;
            this.renderFrame((this.currentFrame + 1) % this.data.frames.length);
        }
    };
    Controller.prototype.pause = function () {
        if (this.playing) {
            this.fireEvent('onStop');
            this.playing = false;
        }
    };
    Controller.prototype.animateTo = function (n) {
        var self = this;
        this.playing = false;
        if (n >= 0 && n < this.data.frames.length) {
            if (n !== this.currentFrame) {
                setTimeout(function () {
                    self.renderFrame((self.currentFrame + 1) % self.data.frames.length);
                    self.animateTo(n);
                }, self.speed);
            }
        }
    };
    Controller.prototype.rewindTo = function (n) {
        var i = 0;
        this.playing = false;
        if (n >= 0 && n < this.data.frames.length) {
            while (i <= n) {
                this.renderFrame(i);
                i += 1;
            }
        }
    };
    Controller.prototype.renderNextFrame = function () {
        this.renderFrame(this.currentFrame + 1);
    };
    Controller.prototype.renderFrame = function (n) {
        var self = this;
        if (n >= self.data.frames.length && self.loop) {
            n = 0;
        }
        if (n < self.data.frames.length) {
            self.currentFrame = n;
            self.renderer.renderFrame(n);
            self.fireEvent('onFrame');
            if (self.playing) {
                setTimeout(function () {
                    self.renderNextFrame();
                }, self.speed);
            }
        } else {
            self.playing = false;
        }
    };
    Controller.prototype.onEvent = function (name, func) {
        this.events[name].push(func);
    };
    Controller.prototype.fireEvent = function (name) {
        var i;
        for (i in this.events[name]) {
            if (this.events[name].hasOwnProperty(i)) {
                this.events[name][i].call(this, this.currentFrame);
            }
        }
    };
    return Controller;
}());
