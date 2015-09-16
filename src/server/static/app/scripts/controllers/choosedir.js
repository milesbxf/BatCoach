'use strict';

/**
 * @ngdoc function
 * @name batcoachApp.controller:AboutCtrl
 * @description # AboutCtrl Controller of the batcoachApp
 */

(function(module) {
	var ChooseDirCtrl = function($scope, $http, $window) {

		$scope.getImportDirectory = function() {
			return $http.get('/api/import/dirname');
		};

		$scope.getBrowserDirectory = function() {
			return $http.get('/api/folders/currentdir').then(function(result) {
				return result.data;
			});
		};

		$scope.folders = [];

		$scope.getFiles = function(folder) {

			var data = {
					path : $scope.directory
				};

			if (folder) {
				data.subdir = folder;
			}
			console.log(data);
			$http.post('/api/folders/list', data).then(function(result) {
				$scope.folders = result.data.folders;
				$scope.directory = result.data.newdir;
			});
		};

		$scope.changeImportDir = function(folder) {
			console.log(folder);
			return $http.post('/api/import/changedir', {
				newdir : folder
			});
		};

		$scope.redirectToImport = function() {
			$window.location.href = '/#/import/';
		};

		$scope.getParent = function() {
			$scope.getFiles('..');
		};

		$scope.directory = '';

		$scope.init = function() {
			console.log('Init');
			$scope.getImportDirectory().then(function(result) {
				$scope.directory = result.data.curDir;
				// start in default directory
				$scope.getFiles();
			});
		};
	};
	module.controller('ChooseDirCtrl', [ '$scope', '$http', '$window',
			ChooseDirCtrl ]);

})(angular.module('batcoachApp'));

// angular.module('batcoachApp')
// .controller('ChooseDirCtrl', );
