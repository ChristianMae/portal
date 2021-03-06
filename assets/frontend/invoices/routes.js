(function () {
  'use strict';

  angular
    .module('invoices.portal')
    .config(routes)
  ;

  function routes ($stateProvider, TEMPLATE_URL) {
    $stateProvider
      .state('invoices', {
        url: '/invoices/',
        onEnter: function (InvoiceService, $q, $state) {

            $q.all([InvoiceService.getLatest()])
            .then(function (response) {
              var invoice = response[0].data;

              if (invoice.code) {
                $state.go('invoiceDetail', {id: invoice.id});
              }

            });

        },
        templateUrl  : TEMPLATE_URL + 'invoice.html',
        controller   : 'InvoiceController',
        controllerAs : 'ctrl'
      })
      .state('invoiceDetail', {
        url          : '/invoices/:id/',
        templateUrl  : TEMPLATE_URL + 'invoice.html',
        controller   : 'InvoiceController',
        controllerAs : 'ctrl'
      })
    ;
  }

})();