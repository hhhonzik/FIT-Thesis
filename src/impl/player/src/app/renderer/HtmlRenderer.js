module.exports = (function () {
    "use strict";
    function HtmlRenderer(element, data, image) {
        var self = this;
        self.element = element;
        self.data = data;
        self.image = image;
        self.canvas = $('<div></div>').css({
            'width': data.size.width,
            'height': data.size.height,
            'position': 'relative'
        });
        self.element.append(self.canvas);
    }
    HtmlRenderer.prototype.renderFrame = function (n) {
        var parts, i, metadata, d;
        this.currentFrame = n;
        parts = this.data.frames[this.currentFrame]; // zmenene casti
        // pokud je prvni slide, muzeme vymazat content
        if (this.canvas && n === 0) {
            this.canvas.html('');
        }
        for (i = 0; i < parts.length; i += 1) {
            metadata = parts[i]; // souradnice
            d = $('<div></div>');
            d.css({
                position: 'absolute',
                left: metadata[4],
                top: metadata[5],
                width: metadata[2],
                height: metadata[3],
                backgroundImage: 'url(' + this.image.src + ')',
                backgroundPosition: "-" + metadata[0] + "px -" + metadata[1] + "px"
            });
            this.canvas.append(d);
        }
    };
    return HtmlRenderer;
}());
