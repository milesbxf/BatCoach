'use strict';

describe('Controller: ImportCtrl', function() {

	// load the controller's module
	beforeEach(module('batcoachApp'));

	var ImportCtrl, scope, fileRequestHandler, dirnameRequestHandler;
	var $httpBackend;
	var files = [ 'pavilion.html', 'squad.html', 'etc.html' ];
	var scopefiles = [ {filename:'pavilion.html',selected:true},{filename:'squad.html',selected:true},{filename:'etc.html',selected:true} ];
	var currentdir = 'testdir';

	// Initialize the controller and a mock scope
	beforeEach(inject(function($controller, $injector, $rootScope, $http) {
		// initialise the mock HTTP backend
		$httpBackend = $injector.get('$httpBackend');

		// initialise some handlers
		fileRequestHandler = $httpBackend.when('GET', '/api/import/listfiles')
				.respond({
					files : files
				});

		dirnameRequestHandler = $httpBackend.when('GET', '/api/import/dirname')
				.respond({
					curDir : currentdir
				});

		scope = $rootScope.$new();
		ImportCtrl = $controller('ImportCtrl', {
			$scope : scope,
			$http : $http
		});
	}));

	afterEach(function() {
		$httpBackend.verifyNoOutstandingExpectation();
		$httpBackend.verifyNoOutstandingRequest();
	});

	it('should get directory name', function() {
		// tests that the current import directory can be
		// retrieved from the backend
		$httpBackend.expectGET('/api/import/dirname');
		scope.getDirectoryName();
		$httpBackend.flush();
		expect(scope.directory).toBe(currentdir);
	});

	it('should set loading to false when files are loaded', function() {
		// tests that the loading flag is set to false once the files are
		// successfully loaded
		scope.init();
		$httpBackend.flush();

		expect(scope.loading).toBe(false);

	});

	it('should set error to invaliddir if a HTTP 500 error occurs', function() {
		//tests the response to a HTTP 500 'Import directory given is invalid' is correct
		fileRequestHandler.respond(500,'Import directory given is invalid');
		$httpBackend.expectGET('/api/import/listfiles');
		
		scope.getFiles();
		$httpBackend.flush();
		
		expect(scope.error).toBe('invaliddir');
	});
	
	it('should get a list of files', function() {
		// tests that a list of HTML files in the current import directory
		// can be retrieved

		$httpBackend.expectGET('/api/import/listfiles');
		scope.getFiles();
		$httpBackend.flush();
		expect(scope.files.length).toBe(3);
	});
	
	it('should send files to the server to import', function() {
		//tests that a HTTP request with the specified files is made
		scope.files = scopefiles;
		
		$httpBackend.expectPOST('/api/import/importfiles', {files: files}).respond(200);
		
		scope.submitFilesForImport();
		
		$httpBackend.flush();
	});

});
