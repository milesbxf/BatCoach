'use strict';

(function(module) {
	var SetupCtrl = function($scope,Upload) {
		
		$scope.$watch('file', function () {
	        if ($scope.file !== null) {
	            $scope.upload($scope.file);
	        }
	    });
		
		$scope.upload = function(file) {
			if(file) {
				Upload.upload({
					url: '/api/import/upload',
					file: file,
					data: file.lastModifiedDate
				});
			}
		};
		
	};
	module.controller('SetupCtrl', [ '$scope','Upload',SetupCtrl ]);
	
	
})(angular.module('batcoachApp'));