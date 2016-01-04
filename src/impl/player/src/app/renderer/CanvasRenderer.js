module.exports = (function () {
    "use strict";
    function CanvasRenderer(element, data, image) {
        var self = this;
        self.element = element;
        self.data = data;
        self.image = image;
        self.canvas = $('<canvas></canvas>').attr('width', data.size.width).attr('height', data.size.height).appendTo(self.element);
        self.context = self.canvas[0].getContext('2d');
    }
    CanvasRenderer.prototype.renderFrame = function (n) {
        var parts, i, metadata;
        this.currentFrame = n;
        parts = this.data.frames[this.currentFrame]; // zmenene casti

        for (i = 0; i < parts.length; i += 1) {
            metadata = parts[i]; // souradnice
            this.context.drawImage.apply( // vykresli zmenenou cast
                this.context,
                [this.image].concat(metadata).concat([metadata[2], metadata[3]])
            );
        }
    };
    return CanvasRenderer;
}());
