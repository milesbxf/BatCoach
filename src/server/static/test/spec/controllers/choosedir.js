'use strict';

describe(
		'Controller: ChooseDirCtrl',
		function() {

			// load the controller's module
			beforeEach(module('batcoachApp'));

			var ChooseDirCtrl, scope, dirnameRequestHandler, folderlistRequestHandler;
			var $httpBackend;
			var currentdir = '~/testdir/', subdir = 'testsubdir', newdir = '~/testdir/testsubdir/';
			var folders = [ 'pavilion.html', 'squad.html', 'etc.html' ];

			// Initialize the controller and a mock scope
			beforeEach(inject(function($controller, $rootScope, $http) {
				scope = $rootScope.$new();
				ChooseDirCtrl = $controller('ChooseDirCtrl', {
					$scope : scope,
					$http : $http
				});
			}));

			beforeEach(inject(function($injector) {
				// initialise the mock HTTP backend
				$httpBackend = $injector.get('$httpBackend');

				dirnameRequestHandler = $httpBackend.when('GET',
						'/api/import/dirname').respond({
					curDir : currentdir
				});

				folderlistRequestHandler = $httpBackend.when('POST',
						'/api/folders/list').respond({
					newdir : currentdir,
					folders : folders
				});

				$httpBackend.expectGET('/api/import/dirname');
				$httpBackend.expectPOST('/api/folders/list', {
					path : currentdir
				});

				scope.init();
				$httpBackend.flush();
			}));

			afterEach(function() {
				$httpBackend.verifyNoOutstandingExpectation();
				$httpBackend.verifyNoOutstandingRequest();
			});

			it('should set browser directory to default directory name',
					function() {

						expect(scope.directory).toBe('~/testdir/');
					});

			it('should get a list of folders from the default directory',
					function() {
						expect(scope.folders).toEqual(folders);
					});

			it('should get a list of folders from the specified subdir',
					function() {

						$httpBackend.expectPOST('/api/folders/list', {
							path : currentdir,
							subdir : subdir
						});
						scope.getFiles(subdir);
						$httpBackend.flush();
					});

			it(
					'should change the directory to the new directory given by the server',
					function() {
						folderlistRequestHandler.respond({
							newdir : newdir,
							folders : folders
						});
						scope.getFiles(subdir);
						$httpBackend.flush();
						expect(scope.directory).toBe(newdir);
					});

			it('should get a list of folders from the parent', function() {

				$httpBackend.expectPOST('/api/folders/list', {
					path : currentdir,
					subdir : '..'
				});

				scope.getParent();
				$httpBackend.flush();

			});

			it('should change the import directory', function() {
				
				$httpBackend.expectPOST('/api/import/changedir',{newdir:currentdir}).respond(200);
				
				scope.changeImportDir(currentdir);
				$httpBackend.flush();
			});
			
		});
