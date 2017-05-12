/**
 * Created by sree on 16/11/16.
 */

(function () {

  'use strict';

  angular
    .module('branch', ['ngMaterial', 'datatables'])
    .config(config);

  /** @ngInject */
  function config($stateProvider) {

        $stateProvider
          .state('list', {
            url: "/branches",
            templateUrl: "/static/angular-src/myapps/branch/list/list.html",
            controller: 'BranchListController as vm',
            data: {
              loginRequired: false
            }
          });

        $stateProvider
          .state('detail', {
            url: "/branches/:branchId",
            templateUrl: "/static/angular-src/myapps/branch/detail/detail.html",
            controller: 'BranchDetailController as vm',
            data: {
              loginRequired: false
            }
          });
      }
})();

