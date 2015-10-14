'use strict';

angular.module('batcoachApp').factory('GlobalsService',
		[ '$http', 'Upload', function($http,Upload) {
			
			var svc = {};
			
			svc.getImportDir = function() {
				return $http.get('/api/import/dirname');
			};
			
			svc.getDBInit = function() {
				return $http.get('/api/config/dbinit');
			};
			
			svc.upload = function(file) {
				if(file) {
					Upload.upload({
						url: '/api/import/upload',
						file: file,
						data: file.lastModifiedDate
					});
				}
			};

			return svc;
		} ]);