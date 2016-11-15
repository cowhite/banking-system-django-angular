/**
 * Created by sree on 16/11/16.
 */
(function () {
    'use strict';
    angular
      .module('auth')
      .controller('SignInController', SignInController);

    function SignInController (signInFactory) {
      var vm = this;

      vm.email = '';
      vm.password = '';
      
      vm.signIn = signIn;

      function signIn() {
        signInFactory.signIn(vm.email, vm.password)
          .then(function (response) {

          });
      }      
    }
  }
)();