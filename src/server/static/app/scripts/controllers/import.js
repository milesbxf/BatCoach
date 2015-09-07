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
		
    $scope.directory = '<Connection error>';
        
    $scope.getDirectoryName = function() {
         $http.get('/api/import/dirname')
    	 .then(function(result) {
    		 $scope.directory = result.data;
    	 }); 
    };
    
    $scope.getFiles = function () {
        $http.get('api/import/listfiles')
            .then(function(result) {
            var listOfFiles = result.data;
            $scope.files = [];
            for (var i = 0; i < listOfFiles.length; i++) {
                $scope.files[i] = {filename:listOfFiles[i],selected:true};
            }
        });
    };
    
        
    $scope.submitFilesForImport = function() {
        var listOfFiles = [];
        
        for (var i = 0; i < $scope.files.length; i++) {
            if($scope.files[i].selected) {
                listOfFiles.push($scope.files[i].filename);
            }
        }
        $http.post('api/import/importfiles',listOfFiles)
            .then(function(response) {
                console.log(response.data)
        });
            
    }; 
    
    $scope.getDirectoryName();
        
    $scope.getFiles();
        
 };
 module.controller('ImportCtrl', ['$scope', '$http', ImportCtrl]);
 
})(angular.module('batcoachApp'));


// angular.module('batcoachApp')
  // .controller('ImportCtrl', );
