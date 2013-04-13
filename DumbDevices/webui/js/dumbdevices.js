angular.module('dumbdevicesServices', ['ngResource']).
  factory('Api', function($resource) {
    return $resource('api/devices/:id/:action', {id: '@id', action: '@action'}, {});
  });

angular.module('dumbdevices', ['dumbdevicesServices']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.
      when('/devices', {controller: DumbDevicesCtrl, templateUrl: 'list.html'}).
      otherwise({redirectTo: '/devices'});
  }]);

function DumbDevicesCtrl($scope, $timeout, Api) {
  function get_devices() {
    Api.query(function(e) { 
      $scope.devices = e;
    });
    $timeout(get_devices, 3000);
  }

  get_devices();
  
  Api.save({id: 'light', action: 'toggle'});
}