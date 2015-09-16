'use strict';

describe('Controller: SquadCtrl', function () {

  // load the controller's module
  beforeEach(module('batcoachApp'));

  var SquadCtrl,
    scope;
var httpLocalBackend;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope,$http) {
    scope = $rootScope.$new();
    SquadCtrl = $controller('SquadCtrl', {
      $scope: scope,
        $http: $http
    });
  }));

    
    beforeEach(inject(function ($httpBackend) {
        httpLocalBackend = $httpBackend;
    }));
    
//  it('should have no players', function () {
//    expect(scope.players).toBeUndefined();
//  });
//    
//    it('should get some players', function() {
//        var players = [       {firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4},{firstName:'John',surName:'Smith',age:18,BTR:3000,wage:812,batAggression:'4',batHand:'R',bowlAggression:'3',bowlHand:'R',bowlType:'M',batForm:9,bowlForm:7,stamina:3,keeping:4,batting:6,concentration:4,bowling:7,consistency:6,fielding:4}];
//        
//        
//        httpLocalBackend.expectGET('/api/players').respond(200,players);
//        scope.getPlayers();
//        httpLocalBackend.flush();
//        expect(scope.players.length).toBe(10);
//    });
});
