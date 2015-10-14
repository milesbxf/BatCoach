'use strict';

(function(module) {
	var SetupCtrl = function($scope,Upload) {
		
		$scope.$watch('file', function () {
	        if ($scope.file !== null) {
	            $scope.upload($scope.file);
	        }
	    });
		
		$scope.upload = GlobalsService.upload;
		
	};
	module.controller('SetupCtrl', [ '$scope','GlobalsService',SetupCtrl ]);
	
	
})(angular.module('batcoachApp'));