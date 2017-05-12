/**
 * Created by sree on 16/11/16.
 */
(function () {
        'use strict';
        angular
            .module('branch')
            .controller('BranchListController', BranchListController);

        function BranchListController (branchListFactory, DTOptionsBuilder, DTColumnBuilder) {
            var vm = this;

            vm.dtInstance = null; // this will be our variable in angular that is referenced to the datatable created (will be set in html)

            vm.dtOptions = getDtOptions();
            vm.dtColumns = getDtColumns();

            function getDtColumns(){
                var columns = [
                    DTColumnBuilder.newColumn('name').withTitle('Name'),
                    DTColumnBuilder.newColumn('company').withTitle('Company').notSortable(),
                    DTColumnBuilder.newColumn('dept.name').withTitle('Department'),
                ];
                return columns;
            }

            function getDtOptions(){
                var options = DTOptionsBuilder.newOptions()
                    .withOption('ajax', {  // this sets the api location for pulling the data to be populated in datatable
                        url: '/branches/',
                        type: 'GET',
                    })
                    .withDataProp('results')  // the array element in the json that is to be populated (in our case 'results')
                    .withOption('processing', true) // to set the processing at serverside
                    .withOption('serverSide', true); // to set the processing at serverside

                return options;
            }

        }
    }
)();