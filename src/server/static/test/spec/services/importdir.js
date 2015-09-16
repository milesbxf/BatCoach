'use strict';

describe('Service: ImportDirService', function() {

	// load the controller's module
	beforeEach(module('batcoachApp'));

	var ImportDirService, scope, dirnameRequestHandler;
	var $httpBackend;
	var currentdir = '~/testdir/';

	// Initialize the controller and a mock scope
	beforeEach(inject(function($service, $rootScope, $http) {
		scope = $rootScope.$new();
		ImportDirService = $service('ImportDirService', {
			$scope : scope,
			$http : $http
		});
	}));

	beforeEach(inject(function($injector) {
		// initialise the mock HTTP backend
		$httpBackend = $injector.get('$httpBackend');

		dirnameRequestHandler = $httpBackend.when('GET', '/api/import/dirname')
				.respond({
					curDir : currentdir
				});
		$httpBackend.expectGET('/api/import/dirname');

		$httpBackend.flush();
	}));

	afterEach(function() {
		$httpBackend.verifyNoOutstandingExpectation();
		$httpBackend.verifyNoOutstandingRequest();
	});

	it('should get import directory', function() {

		expect(scope.getImportDirectory).toBe('~/testdir/');
	});

});