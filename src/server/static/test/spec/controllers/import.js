'use strict';

describe('Controller: ImportCtrl', function () {

  // load the controller's module
  beforeEach(module('batcoachApp'));

  var ImportCtrl,
    scope;
var httpLocalBackend;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope,$http) {
    scope = $rootScope.$new();
    ImportCtrl = $controller('ImportCtrl', {
      $scope: scope,
        $http: $http
    });
  }));

    
    beforeEach(inject(function ($httpBackend) {
        httpLocalBackend = $httpBackend;
    }));
        
    it('should get directory name', function() {
            
        
        httpLocalBackend.expectGET('/api/import/dirname').respond(200,'~/testdir/');
        scope.getDirectoryName();
        httpLocalBackend.flush();
        expect(scope.directory).toBe('~/testdir/');
    });
    
    it('should get a list of files', function() {
        var files = ['pavilion.html','squad.html','etc.html'];
        
        httpLocalBackend.expectGET('/api/import/listfiles').respond(200,files);
        scope.getFiles();
        httpLocalBackend.flush();
        expect(scope.files.length).toBe(3);
    });
});
