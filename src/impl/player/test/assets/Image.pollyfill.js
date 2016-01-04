module.exports = (function () {
    "use strict";
    function Image() {
        this.src = '';
    }
    Image.prototype.onload = function (func) {
        setTimeout(func, 100);
    };
    return Image;
}());
