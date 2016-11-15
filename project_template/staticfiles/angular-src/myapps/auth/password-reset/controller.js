/**
 * Created by sree on 16/11/16.
 */
(function () {
    'use strict';
    angular
      .module('auth')
      .controller('PasswordResetController', PasswordResetController);

    function PasswordResetController () {
      var vm = this;

      vm.username = '';
      vm.email = '';

    }
  }
)();