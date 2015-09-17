'use strict';




angular.module('batcoachApp')
.factory('ImportDirService', ['$http',function($http) {
		var getImportDir = function() {
			return $http.get('/api/import/dirname');
		};
		
		return {
			getImportDir: getImportDir
		};
	}]);