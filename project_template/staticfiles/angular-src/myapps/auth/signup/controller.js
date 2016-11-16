/**
 * Created by sree on 16/11/16.
 */
(function () {
    'use strict';
    angular
      .module('auth')
      .controller('SignUpController', SignUpController);

    function SignUpController (signUpFactory) {
      var vm = this;

      vm.email = '';
      vm.mobile_num = '';
      vm.password1 = '';
      vm.password2 = '';

      vm.signUp = signUp;

      function signUp() {
        signUpFactory.signUp(vm.email, vm.mobile_num, vm.password1, vm.password2)
          .then(function (response) {

          });
      }

    }
  }
)();