function Route(name, htmlName, cssFiles, scripts, defaultRoute) {
    try {
        if (!name || !htmlName) {
            throw 'error: name and htmlName params are mandatory';
        }
        this.constructor(name, htmlName, cssFiles, scripts, defaultRoute);
    } catch (e) {
        console.error(e);
    }
}

Route.prototype = {
    name: undefined,
    htmlName: undefined,
    cssFiles: undefined,
    scripts: undefined,
    default: undefined,
    constructor: function (name, htmlName, cssFiles, scripts, defaultRoute) {
        this.name = name;
        this.htmlName = htmlName;
        this.cssFiles = cssFiles || [];
        this.scripts = scripts || [];
        this.default = defaultRoute;
    },
    isActiveRoute: function (hashedPath) {
        return hashedPath.replace('#', '') === this.name;
    }
}
