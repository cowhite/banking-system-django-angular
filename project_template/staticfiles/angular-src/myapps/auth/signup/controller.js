/**
 * Created by sree on 16/11/16.
 */
(function () {
    'use strict';
    angular
      .module('auth')
      .controller('SignUpController', SignUpController);

    function SignUpController () {
      var vm = this;

      vm.username = '';
      vm.email = '';
      vm.password1 = '';
      vm.password2 = '';



    }
  }
)();