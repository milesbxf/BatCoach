'use strict';

/**
 * @ngdoc function
 * @name batcoachApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the batcoachApp
 */
angular.module('batcoachApp')
  .controller('MainCtrl', [ '$scope','GlobalsService','$window',function($scope,GlobalsService,$window) {
	  	  $scope.init = function() {
	  		GlobalsService.getDBInit().then(function(response) {
	  			  console.log(response.data.dbInit);
	  			  if(!response.data.dbInit) {
	  				$window.location.href = '/#/setup/';
	  			  }
	  		  });
	  	  };
  }]);
