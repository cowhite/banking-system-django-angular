(function () {
  angular.module('appBase', [
    'ui.router',
    'ngMessages',
    'ngMaterial',
    'ngStorage',

    // Custom modules
    'auth'

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
      }
    ]);
})();
