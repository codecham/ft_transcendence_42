'use strict';

function Router(routes) {
    try {
        if (!routes) {
            throw 'error: routes param is mandatory';
        }
        this.constructor(routes);
        this.init();
    } catch (e) {
        console.error(e);   
    }
}

Router.prototype = {
    routes: undefined,
    rootElem: undefined,
    constructor: function (routes) {
        this.routes = routes;
        this.rootElem = document.getElementById('app');
    },


    init: function () {
        var r = this.routes;
        var scope = this; 

        window.addEventListener('hashchange', function (e) {
            scope.hasChanged(scope, r);
        });

        window.addEventListener('popstate', function (e) {
            this.location.reload();
        });
        this.hasChanged(this, r);
    },

    hasChanged: function(scope, r) {
        if (window.location.hash.length > 0) {
            var hashParts = window.location.hash.substr(1).split('?');
            for (var i = 0, length = r.length; i < length; i++) {
                var route = r[i];
                if (route.isActiveRoute(hashParts[0])) {
                    scope.goToRoute(route.htmlName, route.cssFiles, route.scripts, hashParts.slice(1));
                }
            }
        } else {
            for (var i = 0, length = r.length; i < length; i++) {
                var route = r[i];
                if(route.default) {
                    scope.goToRoute(route.htmlName, route.cssFiles, route.scripts);
                }
            }
        }
    },
    

    loadCSSFiles: function (cssFiles) {
        var scope = this;
        for (var i = 0; i < cssFiles.length; i++) {
            var cssFile = cssFiles[i];
            var link = document.createElement('link');
            link.rel = 'stylesheet';
            link.type = 'text/css';
            link.href = "views/" + cssFile;
            scope.rootElem.appendChild(link);
        }
    },


    loadScripts: function (scripts) {
        for (var i = 0; i < scripts.length; i++) {
            var scope = this;
            var script = scripts[i];
            var scriptElement = document.createElement('script');
            scriptElement.src = "views/" + script;
            scriptElement.type = "module";
            scope.rootElem.appendChild(scriptElement);
        }
    },

    goToRoute: async function (htmlName, cssFiles, scripts, params) {
        if ( await this.redirectUser(htmlName)) {
            var scope = this;
            var url = scope.createUrl(htmlName, params)
            var xhttp = new XMLHttpRequest();

            xhttp.onreadystatechange = function () {
                if (this.readyState === 4 && this.status === 200) {
                    scope.rootElem.innerHTML = this.responseText;
                    if (cssFiles) {
                        scope.loadCSSFiles(cssFiles);
                    }
                    if (scripts) {
                        scope.loadScripts(scripts);
                    }
                    if (!params) {
                        params = [];
                    }
                    scope.checkDisplayNavBar(htmlName);
                }
            };
            xhttp.open('GET', url, true);
            xhttp.send();
        }
    },

    checkUserIsLog: async function() {
        console.log("OUIIIIII PUTAAAAAAAAAAAIN");
        const url = backendUrl + '/authentification/user_is_log/';
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: "include",
        });

        if (!response.ok) {
            console.log("Error response: " + response.status)
            return Promise.resolve(false);
        }
        console.log("response: " + response.status)
        const data = await response.json();
        connected_user = data.username;

        return Promise.resolve(true);
    },

    redirectUser: async function(htmlName) {
        var scope = this;
    
        return new Promise((resolve, reject) => {
            scope.checkUserIsLog()
                .then((userIsLog) => {
                    if (userIsLog) {
                        if (htmlName == "auth/signIn/signIn.html" || htmlName == "auth/signUp/signUp.html") {
                            window.location.hash = 'home';
                            resolve(false);
                        } else {
                            resolve(true);
                        }
                    } else {
                        if (htmlName != "auth/signIn/signIn.html" && htmlName != "auth/signUp/signUp.html") {
                            window.location.hash = 'sign-in';
                            resolve(false);
                        } else {
                            resolve(true);
                        }
                    }
                })
                .catch((error) => {
                    console.error("Error checking user log (redirect user):", error);
                    reject(error);
                });
        });
    },

    createUrl: function(htmlName, params) {
        if (!params || params.length === 0)
            return ('views/' + htmlName);
        var paramsObject = {};
        for (var i = 0; i < params.length; i++) {
            var keyValue = params[i].split('=');
            var key = decodeURIComponent(keyValue[0]);
            var value = decodeURIComponent(keyValue[1]);
            paramsObject[key] = value;
        }
        var queryString = Object.keys(params)
            .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
            .join('&');
            return('views/' + htmlName + '?' + queryString);
    },

    checkDisplayNavBar: function(htmlName) {

        if (htmlName == "auth/signIn/signIn.html" || htmlName == "auth/signUp/signUp.html") {
            document.getElementById("nav-bar").style.display = "none";
        }
        else {
            document.getElementById("nav-bar").style.display = "block";
        }
    }
};


