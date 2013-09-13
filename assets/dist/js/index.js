/*! noweibo - v0.0.1 - 2013-09-13
* http://noweibo.com
* Copyright (c) 2013 Codeb Fan; */
angular.module('noweibo.service', [])

angular.module('noweibo.directive', [])

angular.module('noweibo.filter', []).filter('colorFilter', function () {
  return function (input, flag) {
    var colorClasses = ['text-success', 'text-primary', 'text-warning', 'text-danger']
    var colorClass = null
    if (input < 50) {
      colorClass = 'text-success'
    } else if (input < 100) {
      colorClass = 'text-primary'
    } else if (input < 300) {
      colorClass = 'text-warning'
    } else {
      colorClass = 'text-danger'
    }

    return '<span class="' + colorClass + '">' + input + '</span>'
  }
})

window.APP = angular.module(
    'noweiboIndex',
    ['noweibo.service', 'noweibo.directive', 'noweibo.filter']
  )

APP.controller('AppCtrl', ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
  $scope.weibos = []

  $scope.queryWeibo = function () {
    $http({ method: 'GET', url: '/weibo/public' }).success(function (data, status, headers, config) {
      if (data['status'] === 'OK') {
        $scope.weibos = data['data']
      }
    }).error(function (data, status, headers, config) {
      console.log(status)
    })
  }

  var interval = setInterval(function () {
    $scope.queryWeibo()
  }, 60 * 1000)

  $timeout(function () {
    $scope.queryWeibo()
  }, 0)

}])

