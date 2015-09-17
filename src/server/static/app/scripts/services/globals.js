'use strict';

angular.module('batcoachApp').factory('GlobalsService',
		[ '$http', function($http) {
			
			var svc = {};
			
			svc.getImportDir = function() {
				return $http.get('/api/import/dirname');
			};
			
			svc.getDBInit = function() {
				return $http.get('/api/config/dbinit');
			};

			return svc;
		} ]);