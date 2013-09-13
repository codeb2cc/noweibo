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
    'noweiboHome',
    ['noweibo.service', 'noweibo.directive', 'noweibo.filter']
  )

APP.controller('AppCtrl', ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
  $scope.user = null

  $scope.pageIndex = 0
  $scope.pageSize = 9
  $scope.pages = [0, 1, 2, 3, 4, 5, 6]

  $scope.validMethods = ['time', 'repost', 'comment']
  $scope.orderMethod = 'time'

  $scope.weibos = []

  $scope.pageFilter = function (index) {
    var start = $scope.pageIndex * $scope.pageSize
    var end = start + $scope.pageSize
    return index >= start && index < end
  }

  $scope.pageBtnClass = function (index) {
    return index === $scope.pageIndex ? 'active': ''
  }

  $scope.changePage = function (index) {
    $scope.pageIndex = index
  }

  $scope.orderBtnClass = function (method) {
    return method === $scope.orderMethod ? 'active': ''
  }

  $scope.changeOrder = function (method) {
    if ($scope.validMethods.indexOf(method) !== -1) {
      $scope.orderMethod = method
      $scope.pageIndex = 0
    }
  }

  $scope.orderFilter = function () {
    var mapping = {
      'time': 'create_date',
      'repost': 'reposts_count',
      'comment': 'comments_count'
    }
    return mapping[$scope.orderMethod]
  }

  $scope.optionDeleteBtnClass = function () {
    if (!$scope.user) {
      return ''
    }
    return $scope.user['options']['delete'] ? 'active': ''
  }

  $scope.updateUserOptions = function (option) {
    if (option === 'delete') {
      $http({ method: 'POST', url: '/user/option' }).success(function (data, status, headers, config) {
        if (data['status'] === 'OK') {
          $scope.user['options'] = data['data']
        }
      }).error(function (data, status, headers, config) {
        console.log(status)
      })
    }
  }

  $scope.queryWeibo = function () {
    $http({ method: 'GET', url: '/weibo/query' }).success(function (data, status, headers, config) {
        if (data['status'] === 'OK') {
          $scope.weibos = data['data']
        }
      }).error(function (data, status, headers, config) {
        console.log(status)
      })
  }

  $scope.syncWeibo = function () {
    $http({ method: 'POST', url: '/weibo/sync' }).success(function (data, status, headers, config) {
      $scope.queryWeibo()
    }).error(function (data, status, headers, config) {
      console.log(status)
    })
  }

  $scope.syncUser = function () {
    $http({ method: 'GET', url: '/user/info' }).success(function (data, status, headers, config) {
      if (data['status'] === 'OK') {
        $scope.user = data['data']
        $scope.queryWeibo()
      }
    }).error(function (data, status, headers, config) {
      console.log(status)
    })
  }

  $timeout(function () {
    $scope.syncUser()
    $scope.syncWeibo()
  }, 0)

}])

