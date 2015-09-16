'use strict';

/**
 * @ngdoc function
 * @name batcoachApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the batcoachApp
 */

(function(module) {
	var ImportCtrl = function ($scope,$http) {
	
	
	
    $scope.directory = '';
    
    $scope.loading = true;
    $scope.error = '';
    
    $scope.handleError = function(response) {
    	// set error as generic as a catchall
    	$scope.error = 'generic';
    	if(response.status===500) {
    		if(response.data.indexOf('Import directory') === 0) {
        		$scope.error='invaliddir';
    		}
    	}
    };
    
    $scope.getDirectoryName = function() {
         $http.get('/api/import/dirname')
    	 .then(function(result) {
    		 //success
    		 $scope.directory = result.data.curDir;
    	 },
         $scope.handleError); 
    };
    
    
    $scope.getFiles = function () {
        $http.get('/api/import/listfiles')
            .then(function(result) {
            var listOfFiles = result.data.files;
            $scope.files = [];
            for (var i = 0; i < listOfFiles.length; i++) {
                $scope.files[i] = {filename:listOfFiles[i],selected:true};
            }
            $scope.loading = false;
        },
        $scope.handleError
   	 );
    };
    
        
    $scope.submitFilesForImport = function() {
        var listOfFiles = [];
        
        for (var i = 0; i < $scope.files.length; i++) {
            if($scope.files[i].selected) {
                listOfFiles.push($scope.files[i].filename);
            }
        }
        $http.post('/api/import/importfiles',{files:listOfFiles})
            .then(function() {
        });
            
    }; 
    
    $scope.init = function() {
    	$scope.getDirectoryName();
        $scope.getFiles();
    };
        
        
 };
 module.controller('ImportCtrl', ['$scope', '$http', ImportCtrl]);
 
})(angular.module('batcoachApp'));


// angular.module('batcoachApp')
  // .controller('ImportCtrl', );
