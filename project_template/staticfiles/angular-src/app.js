angular.module('appBase', [
    'ui.router',
    'ngMessages',
    'ngMaterial',
    'ngStorage',
])

.config([
    '$stateProvider',
    '$urlRouterProvider',
    '$httpProvider',
    function (
        $stateProvider,
        $urlRouterProvider,
        $httpProvider
    ) {

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';


        $urlRouterProvider.otherwise('/');

        /*$stateProvider
            .state('home', {
                url: "/",
                templateUrl: "/static/src/myapps/cars/templates/home.html",
                controller: 'HomeCtrl as vm',
                data: {
                    loginRequired: false
                }
            })*/
    }
]);