/**
 * Created by sree on 16/11/16.
 */

(function () {

  'use strict';

  angular
    .module('auth', ['ngMaterial'])
    .config(config);

  /** @ngInject */
  function config($stateProvider) {

        $stateProvider
          .state('signup', {
            url: "/auth/signup",
            templateUrl: "/static/angular-src/myapps/auth/signup/signup.html",
            controller: 'SignUpController as vm',
            data: {
              loginRequired: false
            }
          });

        $stateProvider
          .state('signin', {
            url: "/auth/signin",
            templateUrl: "/static/angular-src/myapps/auth/signin/signin.html",
            controller: 'SignInController as vm',
            data: {
              loginRequired: false
            }
          });

        $stateProvider
          .state('password-reset', {
            url: "/auth/password-reset",
            templateUrl: "/static/angular-src/myapps/auth/password-reset/password-reset.html",
            controller: 'PasswordResetController as vm',
            data: {
              loginRequired: false
            }
          });
      }
})();

