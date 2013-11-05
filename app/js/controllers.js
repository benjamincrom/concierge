'use strict';

/* Controllers */

var conciergeApp = angular.module('conciergeApp', []);

conciergeApp.controller('VideoListCtrl', function VideoListCtrl($scope, $http) {
  $http.get('../_ah/api/concierge/v1/concierge').success(function(data) {
    $scope.video_list = data.video_list;
  });
});
