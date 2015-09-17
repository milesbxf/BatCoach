'use strict';

describe('Service: GlobalsService', function() {

	// load the service's module
	beforeEach(module('batcoachApp'));

	var GlobalsService, dirnameRequestHandler, dbinitRequestHandler;
	var $httpBackend;
	var currentdir = '~/testdir/';

	// Initialize the service and a mock scope
	beforeEach(inject(function($injector) {

		GlobalsService = $injector.get('GlobalsService');

		// initialise the mock HTTP backend
		$httpBackend = $injector.get('$httpBackend');

		dirnameRequestHandler = $httpBackend.when('GET', '/api/import/dirname')
				.respond({
					curDir : currentdir
				});

		dbinitRequestHandler = $httpBackend.when('GET', '/api/config/dbinit')
				.respond({
					dbInit: true
				});
		
	}));

	beforeEach(inject(function() {
	}));

	afterEach(function() {
		$httpBackend.verifyNoOutstandingExpectation();
		$httpBackend.verifyNoOutstandingRequest();
	});

	it('should get import directory', function() {
		var result;
		$httpBackend.expectGET('/api/import/dirname');

		GlobalsService.getImportDir().then(function(response) {
			result = response.data.curDir;
		});
		
		$httpBackend.flush();
		expect(result).toBe(currentdir);
	});
	
	it('should check if the database is setup', function() {

		var result;
		$httpBackend.expectGET('/api/config/dbinit');
		
		GlobalsService.getDBInit().then(function(response) {
			result = response.data.dbInit;
		});

		$httpBackend.flush();
		expect(result).toBe(true);
		
	});

});