'use strict';

/**
 * @ngdoc function
 * @name batcoachApp.controller:AboutCtrl
 * @description # AboutCtrl Controller of the batcoachApp
 */
angular.module('batcoachApp').controller(
		'SquadCtrl',
		function($scope, $http) {
			$scope.getPlayers = function() {
				// $scope.players = [
				// {firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4}];
				$http.get('/api/players').then(function(result) {
					$scope.players = result.data;
					console.log($scope.players);
				});
			};

			$scope.attrStrings = [ 'ulss', 'wrth', 'abys', 'wful', 'fble',
					'mdce', 'comp', 'resp', 'prof', 'strg', 'sprb', 'qual',
					'remk', 'wful', 'expt', 'sens', 'exqs', 'mast', 'mrcls',
					'phen', 'elite' ];

			$scope.aggrStrings = [ 'defensive', 'cautious', 'steady',
					'attacking', 'destructive' ];
			
			$scope.fitStrings = [];

			$scope.getPlayers();

			// $scope.players = [
			// {firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4}];
		});
