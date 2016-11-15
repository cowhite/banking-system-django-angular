/**
 * Created by sree on 16/11/16.
 */
(function () {
  'use strict';
  angular
    .module('auth')
    .factory('signInFactory', ['$q', '$http', signInFactory]);


  function signInFactory($q, $http) {
    var factory = {};

    factory.signIn = signIn;

    function signIn(email, password) {
      var deferred = $q.defer();
      $http({
        url     : '/rest-auth/login/',
        method  : 'POST',
        data    : {
          'email'     : email,
          'password'  : password
        }
      })
        .then(
          function success(response) {
            deferred.resolve(response);
          },
          function error(response) {
            deferred.reject(response);
          });
      return deferred.promise;
    }

    return factory;
  }

})();