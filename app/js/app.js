'use strict';

/* App */
var conciergeApp = angular.module('conciergeApp', [
    'ui.bootstrap',
    'ngSanitize',
    'ngTable',
    'ngResource'
]);

/* Config */
conciergeApp.config(function($locationProvider){
    $locationProvider.html5Mode(true).hashPrefix('!');
});

/* Controllers */
conciergeApp.controller('VideoListCtrl',
    function VideoListCtrl($scope, $timeout, $resource, $http, $filter, ngTableParams) {
        var Api = $resource('/_ah/api/concierge/v1/concierge_list');

        $scope.tableParams = new ngTableParams({
            page: 1,            // show first page
            count: 10,          // count per page
            sorting: {
                name: 'asc'     // initial sorting
            }
        }, {
            total: 7255,           // length of data
            getData: function($defer, params) {
                // ajax request to api
                Api.get(params.url(), function(data) {
                    $scope.video_list = data.video_list;
                    $timeout(function() {
                        // update table params
                        // params.total(data.video_list.total);
                        // set new data
                        $defer.resolve(data.video_list.result);
                    }, 500);
                });
            }
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


conciergeApp.directive('loadingContainer', function () {
    return {
        restrict: 'A',
        scope: false,
        link: function(scope, element, attrs) {
            var loadingLayer = angular.element('<div class="loading"></div>');
            element.append(loadingLayer);
            element.addClass('loading-container');
            scope.$watch(attrs.loadingContainer, function(value) {
                loadingLayer.toggleClass('ng-hide', !value);
            });
        }
    };
});
