'use strict';

/* App */
var conciergeApp = angular.module('conciergeApp', [
    'ui.bootstrap',
    'ngSanitize',
    'ngTable'
]);

/* Config */
conciergeApp.config(function($locationProvider){
    $locationProvider.html5Mode(true).hashPrefix('!');
});

/* Controllers */
conciergeApp.controller('VideoListCtrl',
    function VideoListCtrl($scope, $http, $filter, ngTableParams) {
        $http.get('../_ah/api/concierge/v1/concierge_list').success(function(data) {
            $scope.tableParams = new ngTableParams({
                page: 1,            // show first page
                count: 10,          // count per page
                sorting: {
                   "title": "asc"     // initial sorting
                }
            }, {
                total: data.row_list.length, // length of data
                getData: function($defer, params) {
                    // use build-in angular filter
                    var orderedData = params.sorting() ?
                        $filter('orderBy')(data.row_list, params.orderBy()) :
                        data.row_list;

                    $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
                }
            });
        });
    }
);

conciergeApp.controller('DisplayVideoCtrl',
    function DisplayVideoCtrl($scope, $http, $location) {
        var link_prefix = "/_ah/api/concierge/v1/concierge_display/";
        var link = link_prefix.concat($location.search().request_id)
        $http.get(link).success(function(data) {
            $scope.video = data;
        });
    }
);
