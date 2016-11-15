/**
 * Created by sree on 16/11/16.
 */
(function () {
  'use strict';
  angular
    .module('auth')
    .factory('signUpFactory', ['$q', '$http', signUpFactory]);


  function signUpFactory($q, $http) {
    var factory = {};

    factory.signUp = signUp;

    function signUp(email, password1, password2) {
      var deferred = $q.defer();
      $http({
        url     : '/rest-auth/registration/',
        method  : 'POST',
        data    : {
          'email'     : email,
          'password1' : password1,
          'password2' : password2
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