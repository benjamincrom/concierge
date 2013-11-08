'use strict';

/* App */
var conciergeApp = angular.module('conciergeApp', [
    'ngSanitize',
]);

/* Config */
conciergeApp.config(function($locationProvider){
    $locationProvider.html5Mode(true).hashPrefix('!');
});

/* Controllers */
conciergeApp.controller('VideoListCtrl',
  function VideoListCtrl($scope, $http) {
    $http.get('../_ah/api/concierge/v1/concierge_list').success(function(data) {
      $scope.video_list = data.row_list;
    });
  }
);

conciergeApp.controller('DisplayVideoCtrl',
  function DisplayVideoCtrl($scope, $http, $location) {
    var link_prefix = "../_ah/api/concierge/v1/concierge_display/";
    var link = link_prefix.concat($location.search().request_id)
    $http.get(link).success(function(data) {
      $scope.video = data;
    });
  }
);
