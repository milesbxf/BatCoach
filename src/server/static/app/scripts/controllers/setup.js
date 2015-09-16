'use strict';

(function(module) {
	var SetupCtrl = function($scope,Upload,$timeout) {
		
		$scope.$watch('file', function () {
	        if ($scope.file != null) {
	            $scope.upload($scope.file);
	        }
	    });
		
		$scope.upload = function(file) {
			if(file) {
				Upload.upload({
					url: 'url',
					file: file
				});
			}
		};
		
	};
	module.controller('SetupCtrl', [ '$scope','Upload','$timeout',SetupCtrl ]);
	
	
})(angular.module('batcoachApp'));