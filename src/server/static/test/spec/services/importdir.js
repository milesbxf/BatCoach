'use strict';

describe('Service: ImportDirService', function() {

	// load the service's module
	beforeEach(module('batcoachApp'));

	var ImportDirService, dirnameRequestHandler;
	var $httpBackend;
	var currentdir = '~/testdir/';

	// Initialize the service and a mock scope
	beforeEach(inject(function($injector) {

		ImportDirService = $injector.get('ImportDirService');

		// initialise the mock HTTP backend
		$httpBackend = $injector.get('$httpBackend');

		dirnameRequestHandler = $httpBackend.when('GET', '/api/import/dirname')
				.respond({
					curDir : currentdir
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

		ImportDirService.getImportDir().then(function(response) {
			result = response.data.curDir;
		});
		
		$httpBackend.flush();
		expect(result).toBe(currentdir);
	});

});